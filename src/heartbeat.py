from __future__ import annotations

import asyncio
import time
from pathlib import Path


class Heartbeat:
    """Persist heartbeat information to a file at a fixed interval."""

    def __init__(self, path: Path, interval: float) -> None:
        self.path = Path(path)
        self.interval = float(interval)
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start writing heartbeat signals."""

        if self._task is not None:
            return

        self._write_heartbeat()
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        """Stop the heartbeat loop."""

        if self._task is None:
            return

        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        finally:
            self._task = None

    async def _run(self) -> None:
        try:
            while True:
                await asyncio.sleep(self.interval)
                self._write_heartbeat()
        except asyncio.CancelledError:
            raise

    def _write_heartbeat(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(f"{int(time.time())}\n", encoding="utf-8")
