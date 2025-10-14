from __future__ import annotations

import asyncio
import time
from pathlib import Path

from loguru import logger


class Heartbeat:
    """Persist heartbeat information to a file at a fixed interval."""

    def __init__(self, path: Path, interval: float) -> None:
        self.path = Path(path)
        self.interval = float(interval)
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

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

        self._stop_event.set()
        try:
            await asyncio.wait_for(self._task, timeout=5)
        except asyncio.CancelledError as e:
            logger.opt(exception=e).warning("Cancelled heartbeat task.")
        finally:
            self._task = None

    async def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
            except asyncio.CancelledError:
                logger.debug("waiting stop event")
            self._write_heartbeat()

    def _write_heartbeat(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(f"{int(time.time())}\n", encoding="utf-8")
