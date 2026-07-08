from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BacktestEngine:
    """A simple event-driven backtest scaffold for strategy validation."""

    initial_balance: float
    risk_per_trade: float

    def run(self, prices: list[float], strategy_name: str = "regime") -> dict[str, float | int | str]:
        if not prices:
            raise ValueError("prices must not be empty")

        balance = self.initial_balance
        trades = 0
        max_drawdown = 0.0
        peak = self.initial_balance

        for index in range(1, len(prices)):
            if strategy_name == "regime" and prices[index] > prices[index - 1]:
                trades += 1
                balance += balance * self.risk_per_trade
            elif strategy_name == "regime" and prices[index] < prices[index - 1]:
                trades += 1
                balance -= balance * self.risk_per_trade

            if balance > peak:
                peak = balance
            current_drawdown = (peak - balance) / peak if peak > 0 else 0.0
            max_drawdown = max(max_drawdown, current_drawdown)

        return {
            "strategy_name": strategy_name,
            "initial_balance": self.initial_balance,
            "final_equity": round(balance, 2),
            "trades": trades,
            "max_drawdown": round(max_drawdown, 6),
        }
