from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load a JSON configuration file and return a dictionary."""
    config_path = Path(path or "config/example_config.json")
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("Configuration root must be a JSON object")

    return data


def save_config(config: dict[str, Any], path: str | Path) -> None:
    """Persist a configuration dictionary to disk."""
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
