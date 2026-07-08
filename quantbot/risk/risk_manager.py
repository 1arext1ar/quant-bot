from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiskManager:
    """Core guardrails for live trading safety."""

    max_daily_loss: float = 0.02
    max_daily_drawdown: float = 0.05
    max_open_positions: int = 3

    def can_trade(self, balance: float, equity: float, daily_pnl: float, open_positions: int = 0) -> bool:
        if balance <= 0:
            return False

        daily_loss_pct = abs(daily_pnl) / balance if balance else 0.0
        drawdown_pct = (balance - equity) / balance if balance else 0.0

        if daily_loss_pct >= self.max_daily_loss:
            return False
        if drawdown_pct >= self.max_daily_drawdown:
            return False
        if open_positions >= self.max_open_positions:
            return False
        return True
