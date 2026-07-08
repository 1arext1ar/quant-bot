from pathlib import Path

from quantbot.backtest.engine import BacktestEngine
from quantbot.journal.trade_journal import TradeJournal
from quantbot.utils.logging import TradingLogger


def test_backtest_engine_returns_metrics() -> None:
    prices = [1.1000 + (i * 0.0015) for i in range(30)]
    engine = BacktestEngine(initial_balance=10000.0, risk_per_trade=0.01)
    result = engine.run(prices, strategy_name="regime")

    assert result["trades"] >= 0
    assert result["final_equity"] >= 0.0
    assert "max_drawdown" in result


def test_trade_journal_persists_records(tmp_path: Path) -> None:
    journal_path = tmp_path / "trades.jsonl"
    journal = TradeJournal(journal_path)
    journal.record_trade({"symbol": "EURUSD", "side": "buy", "entry": 1.1000, "exit": 1.1050, "pnl": 50.0})

    trades = journal.get_trades()
    assert len(trades) == 1
    assert trades[0]["symbol"] == "EURUSD"


def test_logger_writes_to_file(tmp_path: Path) -> None:
    log_path = tmp_path / "system.log"
    logger = TradingLogger(log_path)
    logger.info("startup ok")

    assert log_path.exists()
    assert "startup ok" in log_path.read_text(encoding="utf-8")
