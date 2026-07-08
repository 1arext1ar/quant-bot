from __future__ import annotations

from statistics import mean, pstdev


class RegimeStrategy:
    """A lightweight regime-aware strategy based on EMA crossover and z-score filtering."""

    def __init__(self, fast_ema: int = 12, slow_ema: int = 26, atr_period: int = 14, entry_zscore: float = 1.8) -> None:
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema
        self.atr_period = atr_period
        self.entry_zscore = entry_zscore

    def _ema(self, values: list[float], period: int) -> float:
        if len(values) < period:
            return sum(values) / len(values) if values else 0.0
        multiplier = 2.0 / (period + 1)
        ema = values[0]
        for value in values[1:]:
            ema = (value * multiplier) + (ema * (1 - multiplier))
        return ema

    def generate_signal(self, prices: list[float]) -> str:
        """Return one of buy/sell/hold based on recent price behaviour."""
        if len(prices) < max(self.fast_ema, self.slow_ema):
            return "hold"

        fast = self._ema(prices[-self.fast_ema :], self.fast_ema)
        slow = self._ema(prices[-self.slow_ema :], self.slow_ema)
        returns = [prices[i] / prices[i - 1] - 1.0 for i in range(1, len(prices))]
        if len(returns) < 2:
            return "hold"

        avg_return = mean(returns[-self.atr_period :])
        deviation = pstdev(returns[-self.atr_period :]) if len(returns[-self.atr_period :]) > 1 else 0.0
        z_score = (avg_return / deviation) if deviation else 0.0

        if fast > slow and z_score > self.entry_zscore:
            return "buy"
        if fast < slow and z_score < -self.entry_zscore:
            return "sell"
        return "hold"
