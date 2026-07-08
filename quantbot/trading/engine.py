from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from quantbot.mt5.connector import MT5Connector
from quantbot.risk.position_sizing import PositionSizer
from quantbot.risk.risk_manager import RiskManager
from quantbot.strategy.regime import RegimeStrategy


@dataclass(slots=True)
class TradingEngine:
    """Single orchestrator for the quantitative trading pipeline."""

    connector: MT5Connector
    strategy: RegimeStrategy | None = None
    risk_manager: RiskManager | None = None
    position_sizer: PositionSizer | None = None

    def __post_init__(self) -> None:
        self.strategy = self.strategy or RegimeStrategy()
        self.risk_manager = self.risk_manager or RiskManager(max_daily_loss=0.02, max_daily_drawdown=0.05)
        self.position_sizer = self.position_sizer or PositionSizer(risk_per_trade=0.01, min_lot=0.01, max_lot=5.0, lot_step=0.01)

    def run_cycle(self, prices: list[float], balance: float, equity: float, daily_pnl: float, symbol: str = "EURUSD") -> dict[str, Any]:
        signal = self.strategy.generate_signal(prices)
        trade_allowed = self.risk_manager.can_trade(balance=balance, equity=equity, daily_pnl=daily_pnl, open_positions=0)

        if signal == "hold" or not trade_allowed:
            return {
                "signal": signal,
                "trade_allowed": trade_allowed,
                "order_status": "skipped",
                "lot_size": 0.0,
                "reason": "no actionable signal or risk block",
            }

        lot_size = self.position_sizer.compute_lot_size(balance=balance, atr=0.0085, stop_distance=0.0085, pip_value=10.0)
        if self.connector.is_connected:
            submitted = self.connector.submit_market_order(symbol, signal, lot_size)
            status = "submitted" if submitted else "rejected"
            reason = None if submitted else self.connector.last_error
        else:
            status = "rejected"
            reason = "MT5 not connected"

        return {
            "signal": signal,
            "trade_allowed": trade_allowed,
            "order_status": status,
            "lot_size": lot_size,
            "reason": reason,
        }
