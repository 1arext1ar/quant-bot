from __future__ import annotations

from quantbot.trading.runner import TradingRunner


if __name__ == "__main__":
    runner = TradingRunner()
    runner.run(iterations=3, interval_seconds=2)
