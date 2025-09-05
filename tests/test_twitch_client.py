import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from twitch.twitch_client import TwichClient


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_client_start_and_stop():
    twitch = object()

    class DummyChat:
        def __init__(self, twitch):
            self.start = Mock()
            self.join = AsyncMock()
            self.stop = Mock()

        def register_event(self, *args, **kwargs):
            pass

        def __await__(self):
            async def _inner():
                return self

            return _inner().__await__()

    with patch("twitch.twitch_client.Chat", DummyChat):
        client = TwichClient(twitch, [])
        await client.start()
        client.chat.start.assert_called_once()
        client.chat.join.assert_called_once()
        client.stop()
        client.chat.stop.assert_called_once()
