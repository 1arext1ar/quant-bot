from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TradeJournal:
    """Append-only trade journal for recording executed and simulated trades."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def record_trade(self, trade: dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(trade, default=str) + "\n")

    def get_trades(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        records: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle.readlines():
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
