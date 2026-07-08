from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PositionSizer:
    """Risk-based position sizing for a trading system."""

    risk_per_trade: float
    min_lot: float
    max_lot: float
    lot_step: float

    def __post_init__(self) -> None:
        if self.risk_per_trade <= 0:
            raise ValueError("risk_per_trade must be positive")
        if self.min_lot <= 0:
            raise ValueError("min_lot must be positive")
        if self.max_lot < self.min_lot:
            raise ValueError("max_lot must be greater than or equal to min_lot")
        if self.lot_step <= 0:
            raise ValueError("lot_step must be positive")

    def compute_lot_size(self, balance: float, atr: float, stop_distance: float, pip_value: float) -> float:
        """Compute a lot size based on risk and stop distance."""
        if balance <= 0:
            raise ValueError("balance must be positive")
        if atr <= 0 or stop_distance <= 0:
            raise ValueError("atr and stop_distance must be positive")
        if pip_value <= 0:
            raise ValueError("pip_value must be positive")

        risk_amount = balance * self.risk_per_trade
        price_risk = atr if atr > stop_distance else stop_distance
        lot_size = risk_amount / (price_risk * pip_value)
        lot_size = max(self.min_lot, min(self.max_lot, lot_size))
        return round(round(lot_size / self.lot_step) * self.lot_step, 2)
