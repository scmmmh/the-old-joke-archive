"""The TOJA background application."""
import asyncio
import logging
import tesserocr

from aiocouch import CouchDB, Document
from aiocouch.attachment import Attachment
from asyncio_mqtt import Client
from concurrent.futures import Executor, ProcessPoolExecutor
from io import BytesIO
from PIL import Image
from typing import Union

from ..setup import setup_meilisearch, reset_meilisearch
from ..utils import mosquitto, couchdb, meilisearch
from ..text_utils import raw_text, annotations


logger = logging.getLogger(__name__)


def ocr_joke(data: bytes) -> dict:
    """Use Tesseract to OCR the text and return a Prosemirror document."""
    with Image.open(BytesIO(data)) as img:
        raw_text = tesserocr.image_to_text(img).strip().replace('--', '—')
    doc = {
        'type': 'doc',
        'content': [
            {
                'type': 'paragraph',
                'content': [
                    {
                        'type': 'text',
                        'text': line
                    }
                ]
            }
            for line in raw_text.split('\n') if line.strip() != ''
        ]
    }
    return doc


async def joke_ocr_listener(client: Client, executor: Executor) -> None:
    """Run OCR on a single joke."""
    async with client.filtered_messages('jokes/+/ocr') as messages:
        await client.subscribe('jokes/+/ocr')
        logger.debug('OCR listener ready')
        async for message in messages:
            topic = message.topic.split('/')
            async with couchdb() as session:
                db = await session['jokes']
                joke = await db[topic[1]]
                image = Attachment(joke, 'image')
                doc = await asyncio.get_event_loop().run_in_executor(executor, ocr_joke, await image.fetch())
                if 'transcriptions' not in joke:
                    joke['transcriptions'] = {}
                joke['transcriptions']['auto'] = doc
                if joke['status'] == 'extraction-verified':
                    joke['status'] = 'auto-transcribed'
                await joke.save()


async def joke_categorise_listener(client: Client, executor: Executor) -> None:
    """Run the categorisation on the final joke text."""
    async with client.filtered_messages('jokes/+/categorise') as messages:
        await client.subscribe('jokes/+/categorise')
        logger.debug('Categorise listener ready')
        async for message in messages:
            topic = message.topic.split('/')
            logger.debug(topic)


async def create_joke_index_doc(session: CouchDB, joke: Document) -> Union[dict, None]:
    """Create the index document for a joke.

    :param session: The CouchDB session to use
    :type session: :class:`~aiocouch.CouchDB`
    :param joke: The joke to create the index document for
    :type joke: :class:`~aiocouch.Document`
    :return: The search document format of the joke or ``None`` if the joke cannot be published
    :return_type: dict or None
    """
    if joke['status'] == 'published' and 'final' in joke['transcriptions']:
        logger.debug(f'Indexing joke {joke["_id"]}')
        sources_db = await session['sources']
        source = await sources_db[joke['source_id']]
        doc = {
            'id': joke['_id'],
            'title': joke['title'],
            'categories': joke['categories'],
            'topics': joke['topics'] if 'topics' in joke else [],
            'text': raw_text(joke['transcriptions']['final']),
        }
        if 'language' in joke and joke['language'].strip():
            doc['language'] = joke['language'].strip()
        if 'title' in source and source['title'].strip():
            doc['publication'] = source['title'].strip()
        if 'subtitle' in source and source['subtitle'].strip():
            doc['section'] = source['subtitle'].strip()
        if 'publisher' in source and source['publisher'].strip():
            doc['publisher'] = source['publisher'].strip()
        if 'date' in source and len(source['date'].strip()) >= 4:
            doc['year'] = int(source['date'][:4])
        annotation_labels = set()
        for annotation in annotations(joke['transcriptions']['final']):
            if annotation['type'] == 'PersonMark':
                annotation_labels.add('person')
            elif annotation['type'] == 'ObjectMark':
                annotation_labels.add('object')
            elif annotation['type'] == 'LocationMark':
                annotation_labels.add('location')
        doc['annotations'] = list(annotation_labels)
        return doc


async def create_joke_topics_doc(joke: Document) -> Union[dict, None]:
    """Create the index document for a joke topic.

    :param joke: The joke to create the index document for
    :type joke: :class:`~aiocouch.Document`
    :return: The search document format of the joke topics or ``None`` if the joke cannot be
             published
    :return_type: dict or None
    """
    if joke['status'] == 'published' and 'topics' in joke:
        return {'id': joke['_id'],
                'keywords': joke['topics']}


async def joke_publish_listener(client: Client, executor: Executor) -> None:
    """Run the publishing process on the final, published joke."""
    search = meilisearch()
    async with client.filtered_messages('jokes/+/publish') as messages:
        await client.subscribe('jokes/+/publish')
        logger.debug('Publish listener ready')
        async for message in messages:
            topic = message.topic.split('/')
            async with couchdb() as session:
                db = await session['jokes']
                # Index the full joke
                doc = await create_joke_index_doc(session, await db[topic[1]])
                if doc:
                    await search.index_document('jokes', doc)
                # Index just the topics
                doc = await create_joke_topics_doc(await db[topic[1]])
                if doc:
                    await search.index_document('joke_topics', doc)


async def recreate_search_indexes(client: Client, executor: Executor) -> None:
    """Recreate and repopulate all search indexes."""
    logger.debug('Re-indexing all published jokes')
    await reset_meilisearch()
    await setup_meilisearch()
    search = meilisearch()
    async with couchdb() as session:
        db = await session['jokes']
        jokes_buffer = []
        topics_buffer = []
        async for joke in db.find({'status': 'published'}):
            # Index the full joke
            doc = await create_joke_index_doc(session, joke)
            if doc:
                jokes_buffer.append(doc)
                if len(jokes_buffer) >= 100:
                    await search.index_documents('jokes', jokes_buffer)
                    jokes_buffer = []
            # Index just the topics
            doc = await create_joke_topics_doc(joke)
            if doc:
                topics_buffer.append(doc)
                if len(topics_buffer) >= 100:
                    await search.index_documents('joke_topics', topics_buffer)
                    topics_buffer = []
        if len(jokes_buffer) > 0:
            await search.index_documents('jokes', jokes_buffer)
        if len(topics_buffer) > 0:
            await search.index_documents('joke_topics', topics_buffer)


async def admin_listener(client: Client, executor: Executor) -> None:
    """Run the backend admin processes."""
    async with client.filtered_messages('admin/+/+') as messages:
        await client.subscribe('admin/+/+')
        logger.debug('Admin listener ready')
        async for message in messages:
            topic = message.topic.split('/')
            if topic[1] == 'search':
                if topic[2] == 're-index':
                    await recreate_search_indexes(client, executor)


async def main() -> None:
    """Connect to Mosquitto and start individual tasks."""
    with ProcessPoolExecutor() as executor:
        async with mosquitto() as client:
            await asyncio.gather(joke_ocr_listener(client, executor),
                                 joke_categorise_listener(client, executor),
                                 joke_publish_listener(client, executor),
                                 admin_listener(client, executor))


def run_background_app() -> None:
    """Start the background application."""
    try:
        logger.debug('Starting up')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug('Shutting down')
    finally:
        logger.debug('Shutdown')
