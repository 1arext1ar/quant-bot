from __future__ import annotations

from typing import Any


class TerminalDashboard:
    """Minimal terminal dashboard for showing the latest system status."""

    def __init__(self) -> None:
        self._state: dict[str, Any] = {}

    def update(self, **state: Any) -> None:
        self._state.update(state)

    def render(self) -> str:
        if not self._state:
            return "No status data available"

        lines = ["=== QuantBot Terminal Dashboard ==="]
        for key, value in self._state.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
