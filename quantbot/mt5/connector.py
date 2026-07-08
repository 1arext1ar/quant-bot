from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MT5Connector:
    """Pragmatic MetaTrader 5 connector with a real-path fallback for environments that have the official package installed."""

    terminal_path: str | None = None
    login: int | None = None
    password: str | None = None
    server: str | None = None
    is_connected: bool = False
    account_info: dict[str, Any] = field(default_factory=dict)

    def connect(self) -> bool:
        try:
            import MetaTrader5 as mt5  # type: ignore
        except Exception:
            self.is_connected = False
            self.account_info = {}
            return False

        if not self.terminal_path:
            self.terminal_path = "C:/Program Files/MetaTrader 5/terminal64.exe"

        if not mt5.initialize(path=self.terminal_path, login=self.login, password=self.password, server=self.server):
            self.is_connected = False
            self.account_info = {}
            return False

        self.is_connected = True
        self.account_info = {
            "login": self.login,
            "server": self.server,
            "balance": 0.0,
            "equity": 0.0,
            "margin": 0.0,
            "free_margin": 0.0,
            "profit": 0.0,
        }
        return True

    def disconnect(self) -> None:
        try:
            import MetaTrader5 as mt5  # type: ignore
        except Exception:
            self.is_connected = False
            self.account_info = {}
            return

        mt5.shutdown()
        self.is_connected = False
        self.account_info = {}

    def get_account_info(self) -> dict[str, Any]:
        if self.is_connected and self.account_info:
            return self.account_info

        return {
            "login": self.login,
            "server": self.server,
            "balance": 10000.0,
            "equity": 10000.0,
            "margin": 0.0,
            "free_margin": 10000.0,
            "profit": 0.0,
            "status": "demo_stub",
        }

    def get_status_summary(self) -> dict[str, Any]:
        if self.is_connected:
            return {
                "connected": True,
                "mode": "live",
                "login": self.login,
                "server": self.server,
            }

        return {
            "connected": False,
            "mode": "demo_stub",
            "login": self.login,
            "server": self.server,
        }
