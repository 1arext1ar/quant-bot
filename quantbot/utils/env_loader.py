from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def load_env_file(path: str | Path | None = None) -> dict[str, Any]:
    """Load values from a .env file into a dictionary."""
    env_path = Path(path or ".env")
    values: dict[str, Any] = {}
    if not env_path.exists():
        return values

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def get_env_value(key: str, default: str | None = None) -> str | None:
    """Return an environment variable or fallback to the .env file value."""
    if key in os.environ:
        return os.environ[key]

    env_values = load_env_file()
    return env_values.get(key, default)
