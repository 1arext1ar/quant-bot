from quantbot.execution.order_manager import Order, OrderManager
from quantbot.monitor.terminal_dashboard import TerminalDashboard
from quantbot.mt5.connector import MT5Connector


def test_order_manager_tracks_orders() -> None:
    manager = OrderManager()
    order = manager.submit_order(Order(symbol="EURUSD", side="buy", volume=0.1, price=1.1000))

    assert order.symbol == "EURUSD"
    assert manager.get_order_summary()["open_orders"] == 1


def test_dashboard_renders_state() -> None:
    dashboard = TerminalDashboard()
    dashboard.update(balance=10000.0, equity=10050.0)

    rendered = dashboard.render()
    assert "balance" in rendered.lower()
    assert "equity" in rendered.lower()


def test_connector_reports_failed_live_order_when_disconnected() -> None:
    connector = MT5Connector()

    success = connector.submit_market_order("EURUSD", "buy", 0.1)

    assert success is False
    assert connector.last_error is not None
