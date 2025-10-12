import json
import os

from litestar import Litestar
from litestar.di import Provide
from loguru import logger
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import InvalidTokenException
from uvicorn import Config, Server

from config import Settings

from .controllers import AuthController
from .services import AuthService


class WrapVar[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    async def __call__(self) -> T:
        return self.value


async def authenticate(settings: Settings) -> Twitch:
    logger.debug("authenticate starting")
    twitch: Twitch = await Twitch(
        app_id=settings.client_id, app_secret=settings.client_secret
    )
    auth = UserAuthenticator(
        twitch, scopes=settings.user_scope, url=settings.callback_url.unicode_string()
    )

    needs_auth = True
    if os.path.exists(settings.storage_path):
        try:
            with open(settings.storage_path) as _f:
                creds = json.load(_f)
            await twitch.set_user_authentication(
                creds["token"], settings.user_scope, creds["refresh"]
            )
        except InvalidTokenException:
            logger.info("stored token invalid, refreshing...")
        else:
            needs_auth = False
    if needs_auth:
        auth_service = AuthService(
            settings.user_scope, auth, twitch, settings.storage_path
        )
        app = Litestar(
            debug=True,
            dependencies={"auth_service": Provide(WrapVar(auth_service))},
            route_handlers=[AuthController],
        )

        config = Config(app=app, host="0.0.0.0", port=settings.port, log_level="info")
        server = Server(config)

        async def _request_shutdown() -> None:
            server.should_exit = True

        auth_service.subscribe_on_complete(_request_shutdown)

        logger.info("run uvicorn")
        await server.serve()

    logger.info("authenticate [bold green]complete[/]")
    return twitch
