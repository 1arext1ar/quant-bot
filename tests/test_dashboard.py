from quantbot.monitor.terminal_dashboard import TerminalDashboard


def test_dashboard_renders_status_sections() -> None:
    dashboard = TerminalDashboard()
    dashboard.update(balance=10000.0, equity=10120.0, mt5_status="connected", open_orders=1)

    rendered = dashboard.render()
    assert "QuantBot Terminal Dashboard" in rendered
    assert "ACCOUNT" in rendered
    assert "TRADING" in rendered
