from __future__ import annotations

import logging
from pathlib import Path
from typing import TextIO


class TradingLogger:
    """Lightweight structured logger for trading system events."""

    def __init__(self, log_path: str | Path | None = None, stream: TextIO | None = None) -> None:
        self.logger = logging.getLogger("quantbot")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        if log_path is not None:
            path = Path(log_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if stream is not None:
            stream_handler = logging.StreamHandler(stream)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)
