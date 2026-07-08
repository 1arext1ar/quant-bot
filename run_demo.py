from __future__ import annotations

import os
import time
from pathlib import Path

from quantbot.backtest.engine import BacktestEngine
from quantbot.execution.order_manager import Order, OrderManager
from quantbot.journal.trade_journal import TradeJournal
from quantbot.monitor.terminal_dashboard import TerminalDashboard
from quantbot.mt5.connector import MT5Connector
from quantbot.risk.position_sizing import PositionSizer
from quantbot.risk.risk_manager import RiskManager
from quantbot.strategy.regime import RegimeStrategy
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

    strategy = RegimeStrategy(
        fast_ema=config["strategy"].get("fast_ema", 12),
        slow_ema=config["strategy"].get("slow_ema", 26),
        atr_period=config["strategy"].get("atr_period", 14),
        entry_zscore=config["strategy"].get("entry_zscore", 1.8),
    )
    sizer = PositionSizer(
        risk_per_trade=config["account"].get("risk_per_trade", 0.01),
        min_lot=config["risk"].get("min_lot", 0.01),
        max_lot=config["risk"].get("max_lot", 5.0),
        lot_step=config["risk"].get("lot_step", 0.01),
    )

    prices = [1.1000 + i * 0.0002 for i in range(40)]
    signal = strategy.generate_signal(prices)
    lot_size = sizer.compute_lot_size(balance=10000.0, atr=0.0085, stop_distance=0.0085, pip_value=10.0)
    backtest = BacktestEngine(initial_balance=10000.0, risk_per_trade=0.01)
    metrics = backtest.run(prices, strategy_name="regime")

    journal = TradeJournal("logs/trades.jsonl")
    journal.record_trade({"symbol": "EURUSD", "side": signal, "entry": prices[0], "exit": prices[-1], "pnl": 120.0})

    manager = OrderManager()
    risk_manager = RiskManager(max_daily_loss=0.02, max_daily_drawdown=0.05)
    trade_allowed = risk_manager.can_trade(balance=10000.0, equity=10000.0 + 120.0, daily_pnl=120.0, open_positions=0)

    if trade_allowed:
        manager.submit_order(Order(symbol="EURUSD", side=signal, volume=lot_size, price=prices[-1]))
    else:
        logger.warning("Trade blocked by risk manager")

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
                signal=signal,
                lot=lot_size,
                open_orders=manager.get_order_summary()["open_orders"],
                trade_allowed=trade_allowed,
                runtime="live",
                last_update=time.strftime("%H:%M:%S"),
                messages=["system running", "risk checks active"],
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
