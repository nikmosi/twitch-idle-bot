import asyncio

from loguru import logger

from config.settings import Settings
from heartbeat import Heartbeat
from twitch.twitch_auth import authenticate
from twitch.twitch_client import TwichClient


async def main():
    logger.debug("start")
    settings = Settings()
    twitch = await authenticate(settings)
    client = TwichClient(twitch, settings.target_channels)
    heartbeat = Heartbeat(
        path=settings.heartbeat_path,
        interval=settings.heartbeat_interval_seconds,
    )

    try:
        await heartbeat.start()
        await client.start()
        while True:
            logger.info("live")
            await asyncio.sleep(60)
    finally:
        client.stop()
        await heartbeat.stop()
        await twitch.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
