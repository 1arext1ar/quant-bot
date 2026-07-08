from quantbot.mt5.connector import MT5Connector
from quantbot.risk.risk_manager import RiskManager


def test_mt5_connector_reports_unavailable_when_dependency_missing() -> None:
    connector = MT5Connector()
    assert connector.connect() is False
    assert connector.is_connected is False


def test_risk_manager_blocks_trade_on_daily_loss_limit() -> None:
    manager = RiskManager(max_daily_loss=0.02, max_daily_drawdown=0.05)
    allowed = manager.can_trade(balance=10000.0, equity=9800.0, daily_pnl=-250.0)
    assert allowed is False


def test_risk_manager_allows_trade_when_within_limit() -> None:
    manager = RiskManager(max_daily_loss=0.02, max_daily_drawdown=0.05)
    allowed = manager.can_trade(balance=10000.0, equity=10050.0, daily_pnl=100.0)
    assert allowed is True
