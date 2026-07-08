from __future__ import annotations

import os
import time
from pathlib import Path

from quantbot.backtest.engine import BacktestEngine
from quantbot.execution.order_manager import Order, OrderManager
from quantbot.journal.trade_journal import TradeJournal
from quantbot.monitor.terminal_dashboard import TerminalDashboard
from quantbot.mt5.connector import MT5Connector
from quantbot.trading.engine import TradingEngine
from quantbot.utils.config import load_config
from quantbot.utils.env_loader import get_env_value
from quantbot.utils.logging import TradingLogger


def main() -> None:
    config = load_config(Path("config/example_config.json"))
    run_forever = True
    logger = TradingLogger("logs/demo.log")
    logger.info("QuantBot demo started")

    demo_login = get_env_value("MT5_LOGIN")
    demo_server = get_env_value("MT5_SERVER")
    connector = MT5Connector(
        terminal_path=get_env_value("MT5_TERMINAL_PATH"),
        login=int(demo_login) if demo_login and demo_login.isdigit() else None,
        password=get_env_value("MT5_PASSWORD"),
        server=demo_server,
    )
    mt5_connected = connector.connect()
    mt5_status = connector.get_status_summary()

    if demo_login:
        logger.info(f"Demo MT5 login configured: {demo_login}")
    if demo_server:
        logger.info(f"Demo MT5 server configured: {demo_server}")
    logger.info(f"MT5 connection status: {mt5_status}")

    prices = [1.1000 + i * 0.0002 for i in range(40)]
    backtest = BacktestEngine(initial_balance=10000.0, risk_per_trade=0.01)
    metrics = backtest.run(prices, strategy_name="regime")
    logger.info(f"Backtest metrics: {metrics}")

    journal = TradeJournal("logs/trades.jsonl")
    manager = OrderManager()
    engine = TradingEngine(connector=connector)

    cycle_result = engine.run_cycle(prices, balance=10000.0, equity=10000.0 + 120.0, daily_pnl=120.0)
    signal = cycle_result["signal"]
    lot_size = cycle_result["lot_size"]
    trade_allowed = cycle_result["trade_allowed"]

    messages = ["system running", "risk checks active"]
    if cycle_result["order_status"] == "submitted":
        manager.submit_order(Order(symbol="EURUSD", side=signal, volume=lot_size, price=prices[-1]))
        journal.record_trade({"symbol": "EURUSD", "side": signal, "entry": prices[0], "exit": prices[-1], "pnl": 120.0})
        messages.append("MT5 order submitted")
    elif cycle_result["order_status"] == "rejected":
        reason = cycle_result.get("reason") or "MT5 order submission failed"
        messages.append(reason)
        logger.warning(reason)
    else:
        logger.info("No trade executed this cycle")

    dashboard = TerminalDashboard()
    dashboard.update(balance=10000.0, equity=10000.0 + 120.0, open_orders=manager.get_order_summary()["open_orders"], trade_allowed=trade_allowed)

    while run_forever:
        try:
            os.system("cls" if os.name == "nt" else "clear")
            dashboard.update(
                balance=10000.0,
                equity=10000.0 + 120.0,
                margin=500.0,
                free_margin=9500.0,
                mt5_status=mt5_status["mode"],
                mt5_login=mt5_status.get("login"),
                mt5_server=mt5_status.get("server"),
                mt5_last_error=connector.last_error,
                signal=signal,
                lot=lot_size,
                open_orders=manager.get_order_summary()["open_orders"],
                trade_allowed=trade_allowed,
                runtime="live",
                last_update=time.strftime("%H:%M:%S"),
                messages=messages + ([connector.last_error] if connector.last_error else []),
            )
            print(dashboard.render())
            print("-" * 40)
            time.sleep(5)
        except KeyboardInterrupt:
            logger.warning("Interrupted by user")
            break
        except Exception as exc:  # pragma: no cover - defensive runtime guard
            logger.error(f"Runtime loop error: {exc}")
            time.sleep(5)

    logger.info("Demo completed successfully")


if __name__ == "__main__":
    main()
