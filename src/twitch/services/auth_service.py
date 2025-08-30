import json
from collections.abc import Callable
from pathlib import Path
from typing import cast

from loguru import logger
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope

from ..exceptions import CodeError, StateError


class AuthService:
    def __init__(
        self,
        user_scope: list[AuthScope],
        auth: UserAuthenticator,
        twitch: Twitch,
        storage_path: Path,
    ) -> None:
        self.user_scope = user_scope
        self.auth = auth
        self.twitch = twitch
        self.on_complete: list[Callable[[], None]] = []
        self.storage_path = storage_path

    def get_link(self) -> str:
        return cast(str, self.auth.return_auth_url())  # type: ignore[no-untyped-call]

    async def verify(self, code: str | None, state: str | None) -> None:
        if state != self.auth.state:
            raise StateError()
        if code is None:
            raise CodeError()
        token, refresh = cast(
            tuple[str, str], await self.auth.authenticate(user_token=code)
        )
        logger.warning(self.storage_path.resolve())
        with open(self.storage_path, "w") as _f:
            json.dump({"token": token, "refresh": refresh}, _f)
        await self.twitch.set_user_authentication(token, self.user_scope, refresh)

    def subscribe_on_complete(self, callback: Callable[[], None]) -> None:
        self.on_complete.append(callback)

    def complete(self) -> None:
        for func in self.on_complete:
            func()
