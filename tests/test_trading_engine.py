from quantbot.mt5.connector import MT5Connector
from quantbot.trading.engine import TradingEngine


def test_engine_reports_clear_order_status() -> None:
    engine = TradingEngine(connector=MT5Connector())
    result = engine.run_cycle([1.1000 + i * 0.0002 for i in range(40)], balance=10000.0, equity=10000.0, daily_pnl=0.0)

    assert result["signal"] in {"buy", "sell", "hold"}
    assert result["order_status"] in {"skipped", "rejected", "submitted"}
    assert result["trade_allowed"] is True
