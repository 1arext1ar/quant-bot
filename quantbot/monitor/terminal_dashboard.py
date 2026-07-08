from __future__ import annotations

from typing import Any


class TerminalDashboard:
    """Lightweight terminal dashboard for monitoring the trading system in a long-running session."""

    def __init__(self) -> None:
        self._state: dict[str, Any] = {}

    def update(self, **state: Any) -> None:
        self._state.update(state)

    def render(self) -> str:
        if not self._state:
            return "No status data available"

        account = {
            "balance": self._state.get("balance", 0.0),
            "equity": self._state.get("equity", 0.0),
            "margin": self._state.get("margin", 0.0),
            "free_margin": self._state.get("free_margin", 0.0),
        }
        mt5 = {
            "status": self._state.get("mt5_status", "unknown"),
            "login": self._state.get("mt5_login", "-"),
            "server": self._state.get("mt5_server", "-"),
            "last_error": self._state.get("mt5_last_error", "-"),
        }
        trading = {
            "signal": self._state.get("signal", "hold"),
            "lot": self._state.get("lot", 0.0),
            "open_orders": self._state.get("open_orders", 0),
            "trade_allowed": self._state.get("trade_allowed", False),
        }
        system = {
            "runtime": self._state.get("runtime", "0s"),
            "last_update": self._state.get("last_update", "n/a"),
            "messages": self._state.get("messages", []),
        }

        lines = ["=== QuantBot Terminal Dashboard ===", "", "[ACCOUNT]"]
        for key, value in account.items():
            lines.append(f"  {key:<12} {value}")

        lines.extend(["", "[MT5]"])
        for key, value in mt5.items():
            lines.append(f"  {key:<12} {value}")

        lines.extend(["", "[TRADING]"])
        for key, value in trading.items():
            lines.append(f"  {key:<12} {value}")

        lines.extend(["", "[SYSTEM]"])
        for key, value in system.items():
            if key == "messages":
                msgs = value if isinstance(value, list) else [str(value)]
                lines.append(f"  {key:<12} {', '.join(msgs) if msgs else 'none'}")
            else:
                lines.append(f"  {key:<12} {value}")

        return "\n".join(lines)
