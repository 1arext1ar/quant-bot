from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Order:
    symbol: str
    side: str
    volume: float
    price: float | None = None
    stop_loss: float | None = None
    take_profit: float | None = None
    comment: str = ""


@dataclass(slots=True)
class OrderManager:
    """Simple in-memory order manager for a trading engine."""

    orders: list[Order] = field(default_factory=list)

    def submit_order(self, order: Order) -> Order:
        self.orders.append(order)
        return order

    def cancel_order(self, symbol: str, side: str) -> None:
        self.orders = [order for order in self.orders if not (order.symbol == symbol and order.side == side)]

    def get_open_orders(self) -> list[Order]:
        return list(self.orders)

    def get_order_summary(self) -> dict[str, Any]:
        return {
            "open_orders": len(self.orders),
            "symbols": sorted({order.symbol for order in self.orders}),
        }
