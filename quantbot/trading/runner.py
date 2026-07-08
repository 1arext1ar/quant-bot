from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from quantbot.execution.order_manager import Order, OrderManager
from quantbot.journal.trade_journal import TradeJournal
from quantbot.monitor.terminal_dashboard import TerminalDashboard
from quantbot.mt5.connector import MT5Connector
from quantbot.trading.engine import TradingEngine
from quantbot.utils.config import load_config
from quantbot.utils.env_loader import get_env_value
from quantbot.utils.logging import TradingLogger


class TradingRunner:
    """Simple live-style runner that executes trading cycles in a loop."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config = load_config(config_path or Path("config/example_config.json"))
        self.logger = TradingLogger("logs/live.log")
        self.connector = MT5Connector(
            terminal_path=get_env_value("MT5_TERMINAL_PATH"),
            login=int(get_env_value("MT5_LOGIN", "0")) if get_env_value("MT5_LOGIN", "0").isdigit() else None,
            password=get_env_value("MT5_PASSWORD"),
            server=get_env_value("MT5_SERVER"),
        )
        self.engine = TradingEngine(connector=self.connector)
        self.order_manager = OrderManager()
        self.journal = TradeJournal("logs/trades.jsonl")
        self.dashboard = TerminalDashboard()
        self.last_cycle: dict[str, Any] | None = None

    def run(self, iterations: int | None = None, interval_seconds: int = 5) -> None:
        self.logger.info("Trading runner started")
        cycle = 0
        while iterations is None or cycle < iterations:
            try:
                prices = [1.1000 + i * 0.0002 for i in range(40)]
                result = self.engine.run_cycle(prices, balance=10000.0, equity=10000.0 + 120.0, daily_pnl=120.0)
                self.last_cycle = result
                self.logger.info(f"Cycle {cycle + 1}: {result}")

                if result["order_status"] == "submitted":
                    self.order_manager.submit_order(Order(symbol="EURUSD", side=result["signal"], volume=result["lot_size"], price=prices[-1]))
                    self.journal.record_trade({"symbol": "EURUSD", "side": result["signal"], "entry": prices[0], "exit": prices[-1], "pnl": 120.0})

                self.dashboard.update(
                    balance=10000.0,
                    equity=10000.0 + 120.0,
                    margin=500.0,
                    free_margin=9500.0,
                    mt5_status=self.connector.get_status_summary()["mode"],
                    mt5_login=self.connector.login,
                    mt5_server=self.connector.server,
                    mt5_last_error=self.connector.last_error,
                    signal=result["signal"],
                    lot=result["lot_size"],
                    open_orders=self.order_manager.get_order_summary()["open_orders"],
                    trade_allowed=result["trade_allowed"],
                    runtime="live",
                    last_update=time.strftime("%H:%M:%S"),
                    messages=["system running", "risk checks active", result.get("reason") or "idle"],
                )
                print(self.dashboard.render())
                print("-" * 40)
                cycle += 1
                if iterations is not None and cycle >= iterations:
                    break
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                self.logger.warning("Interrupted by user")
                break
            except Exception as exc:  # pragma: no cover - defensive runtime guard
                self.logger.error(f"Runner loop error: {exc}")
                time.sleep(interval_seconds)

        self.logger.info("Trading runner completed")
