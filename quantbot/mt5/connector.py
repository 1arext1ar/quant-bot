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
    last_error: str | None = None

    def connect(self) -> bool:
        self.last_error = None
        try:
            import MetaTrader5 as mt5  # type: ignore
        except Exception as exc:
            self.is_connected = False
            self.account_info = {}
            self.last_error = f"MetaTrader5 package unavailable: {exc}"
            return False

        if not self.terminal_path:
            self.terminal_path = "C:/Program Files/MetaTrader 5/terminal64.exe"

        if not mt5.initialize(path=self.terminal_path, login=self.login, password=self.password, server=self.server):
            self.is_connected = False
            self.account_info = {}
            self.last_error = "MetaTrader5 initialize failed"
            return False

        self.is_connected = True
        self.last_error = None
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
            self.last_error = "MetaTrader5 package unavailable"
            return

        mt5.shutdown()
        self.is_connected = False
        self.account_info = {}
        self.last_error = None

    def submit_market_order(self, symbol: str, side: str, volume: float) -> bool:
        if not self.is_connected:
            self.last_error = "MT5 is not connected"
            return False

        try:
            import MetaTrader5 as mt5  # type: ignore
        except Exception as exc:
            self.last_error = f"MetaTrader5 package unavailable: {exc}"
            return False

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": mt5.ORDER_TYPE_BUY if side.lower() == "buy" else mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).ask if side.lower() == "buy" else mt5.symbol_info_tick(symbol).bid,
            "deviation": 10,
            "magic": 1000,
            "comment": "QuantBot live",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            self.last_error = f"MT5 order rejected: {getattr(result, 'comment', 'unknown')}"
            return False

        self.last_error = None
        return True

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
