import asyncio

from loguru import logger

from config.settings import Settings
from twitch.twitch_auth import authenticate
from twitch.twitch_client import TwichClient


async def main():
    logger.debug("start")
    settings = Settings()
    twitch = await authenticate(settings)
    client = TwichClient(twitch, settings.target_channels)
    try:
        await client.start()
    finally:
        client.stop()
        await twitch.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
