import asyncio
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from heartbeat import Heartbeat


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_heartbeat_writes_and_updates_file(tmp_path: Path) -> None:
    heartbeat_file = tmp_path / "heartbeat"
    heartbeat = Heartbeat(heartbeat_file, interval=0.01)

    await heartbeat.start()
    try:
        await asyncio.sleep(0.02)
        first_mtime = heartbeat_file.stat().st_mtime
        first_value = heartbeat_file.read_text(encoding="utf-8").strip()

        await asyncio.sleep(0.02)
        second_mtime = heartbeat_file.stat().st_mtime
        second_value = heartbeat_file.read_text(encoding="utf-8").strip()
    finally:
        await heartbeat.stop()

    assert heartbeat_file.exists()
    assert first_value.isdigit()
    assert second_value.isdigit()
    assert second_mtime >= first_mtime
    assert (second_mtime > first_mtime) or (second_value != first_value)


@pytest.mark.anyio
async def test_heartbeat_stop_is_idempotent(tmp_path: Path) -> None:
    heartbeat_file = tmp_path / "heartbeat"
    heartbeat = Heartbeat(heartbeat_file, interval=0.01)

    await heartbeat.start()
    await heartbeat.stop()

    # Multiple stops should not raise
    await heartbeat.stop()

    assert heartbeat_file.exists()
