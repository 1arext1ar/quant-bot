import json
from pathlib import Path

import pytest

from quantbot.risk.position_sizing import PositionSizer
from quantbot.strategy.regime import RegimeStrategy
from quantbot.utils.config import load_config


@pytest.fixture
def config_path(tmp_path: Path) -> Path:
    config = {
        "account": {"risk_per_trade": 0.01, "max_daily_loss": 0.02, "max_daily_profit": 0.04},
        "strategy": {"fast_ema": 12, "slow_ema": 26, "atr_period": 14, "entry_zscore": 1.8},
        "risk": {"min_lot": 0.01, "max_lot": 5.0, "lot_step": 0.01},
        "symbols": [{"name": "EURUSD", "timeframe": "H1"}],
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def test_load_config_reads_json(config_path: Path) -> None:
    cfg = load_config(config_path)
    assert cfg["account"]["risk_per_trade"] == 0.01
    assert cfg["symbols"][0]["name"] == "EURUSD"


def test_position_sizer_computes_lot_size() -> None:
    sizer = PositionSizer(risk_per_trade=0.01, min_lot=0.01, max_lot=5.0, lot_step=0.01)
    lot = sizer.compute_lot_size(balance=10000.0, atr=0.0085, stop_distance=0.0085, pip_value=10.0)
    assert lot > 0.0
    assert lot <= 5.0


def test_strategy_emits_signal_for_sample_prices() -> None:
    strategy = RegimeStrategy(fast_ema=12, slow_ema=26, atr_period=14, entry_zscore=1.8)
    prices = [1.1000, 1.1010, 1.1020, 1.1030, 1.1040, 1.1050, 1.1060, 1.1070, 1.1080, 1.1090]
    signal = strategy.generate_signal(prices)
    assert signal in {"buy", "sell", "hold"}
