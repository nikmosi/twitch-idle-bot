from typing import Annotated

from litestar import Controller, MediaType, get, status_codes
from litestar.params import Parameter
from litestar.response import Redirect, Response
from loguru import logger
from twitchAPI.type import TwitchAPIException

from ..exceptions import CodeError, StateError
from ..services import AuthService


class AuthController(Controller):
    @get("/login")
    async def login(self, auth_service: AuthService) -> Redirect:
        logger.debug("generating auth link")
        return Redirect(auth_service.get_link())

    @get("/login/confirm", media_type=MediaType.TEXT)
    async def login_confirm(
        self,
        code: str,
        state_: Annotated[str, Parameter(query="state")],
        auth_service: AuthService,
    ) -> Response[str]:
        logger.debug("compliting auth")
        msg: str = "Auth complete. You can close this tab."
        exit_code = status_codes.HTTP_200_OK
        try:
            await auth_service.verify(code, state_)
        except TwitchAPIException:
            msg = "Auth failed"
            exit_code = status_codes.HTTP_400_BAD_REQUEST
        except StateError:
            msg = "Bad state"
            exit_code = status_codes.HTTP_401_UNAUTHORIZED
        except CodeError:
            msg = "Missing code"
            exit_code = status_codes.HTTP_400_BAD_REQUEST
        else:
            auth_service.complete()
            logger.info("complete auth")
        # FIX: Literal[Auth ...] instead str type
        return Response(str(msg), status_code=exit_code)
