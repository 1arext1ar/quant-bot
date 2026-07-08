from quantbot.trading.runner import TradingRunner


def test_runner_initializes_with_config() -> None:
    runner = TradingRunner()

    assert runner.order_manager is not None
    assert runner.dashboard is not None
    assert runner.engine is not None
