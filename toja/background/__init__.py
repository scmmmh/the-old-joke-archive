"""The TOJA background application."""
import asyncio
import logging
import tesserocr

from aiocouch.attachment import Attachment
from asyncio_mqtt import Client
from concurrent.futures import Executor, ProcessPoolExecutor
from io import BytesIO
from PIL import Image

from ..utils import mosquitto, couchdb, meilisearch
from ..text_utils import raw_text


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
        async for message in messages:
            topic = message.topic.split('/')
            logger.debug(topic)


async def joke_publish_listener(client: Client, executor: Executor) -> None:
    """Run the publishing process on the final, published joke."""
    search = meilisearch()
    async with client.filtered_messages('jokes/+/publish') as messages:
        await client.subscribe('jokes/+/publish')
        async for message in messages:
            topic = message.topic.split('/')
            async with couchdb() as session:
                db = await session['jokes']
                joke = await db[topic[1]]
                if 'final' in joke['transcriptions']:
                    logger.debug(f'Indexing joke {joke["_id"]}')
                    await search.index_document('jokes', {
                        'id': joke['_id'],
                        'title': joke['title'],
                        'categories': joke['categories'],
                        'language': joke['language'],
                        'topics': joke['topics'].split('\n'),
                        'text': raw_text(joke['transcriptions']['final'])
                    })


async def main() -> None:
    """Connect to Mosquitto and start individual tasks."""
    with ProcessPoolExecutor() as executor:
        async with mosquitto() as client:
            await asyncio.gather(joke_ocr_listener(client, executor),
                                 joke_categorise_listener(client, executor),
                                 joke_publish_listener(client, executor))


def run_background_app() -> None:
    """Start the background application."""
    try:
        logger.debug('Starting up')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug('Shutting down')
    finally:
        logger.debug('Shutdown')
