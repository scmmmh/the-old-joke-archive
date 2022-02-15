"""The TOJA background application."""
import asyncio

from asyncio_mqtt import Client

from ..utils import mosquitto


async def joke_ocr(client: Client) -> None:
    """Run OCR on a single joke."""
    async with client.filtered_messages('jokes/+/ocr') as messages:
        await client.subscribe('jokes/+/ocr')
        async for message in messages:
            pass
            # print('Run OCR for', message.topic.split('/')[1])


async def main() -> None:
    """Connect to Mosquitto and start individual tasks."""
    async with mosquitto() as client:
        await asyncio.gather(joke_ocr(client))


def run_background_app() -> None:
    """Start the background application."""
    asyncio.run(main())
