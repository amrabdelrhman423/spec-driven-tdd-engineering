from dataclasses import dataclass
from enum import Enum
from typing import List

class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class InvalidStateTransitionError(ValueError):
    """Raised when an invalid order status transition is attempted."""
    pass

@dataclass(frozen=True)
class OrderItem:
    sku: str
    unit_price: float
    quantity: int

    def __post_init__(self):
        if self.unit_price < 0:
            raise ValueError(f"Unit price cannot be negative: {self.unit_price}")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")

class OrderProcessor:
    """Processes order totals and state transitions adhering strictly to SDD spec."""

    TAX_RATE: float = 0.08

    def calculate_total(self, items: List[OrderItem], is_vip: bool = False) -> float:
        """Calculates grand total including tiered discounts, VIP status, and tax."""
        if not items:
            return 0.0

        subtotal = sum(item.unit_price * item.quantity for item in items)
        
        # Tiered discount
        if subtotal >= 100.0:
            tier_discount_rate = 0.10
        elif subtotal >= 50.0:
            tier_discount_rate = 0.05
        else:
            tier_discount_rate = 0.0

        after_tier = subtotal * (1.0 - tier_discount_rate)

        # VIP discount
        if is_vip:
            after_vip = after_tier * 0.95
        else:
            after_vip = after_tier

        # Tax calculation
        total = after_vip * (1.0 + self.TAX_RATE)
        return round(total, 2)

    def transition_state(self, current: OrderStatus, target: OrderStatus) -> OrderStatus:
        """Transitions order state safely adhering to domain state machine."""
        allowed_transitions = {
            OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELLED},
            OrderStatus.PAID: set(),
            OrderStatus.CANCELLED: set(),
        }

        if target not in allowed_transitions.get(current, set()):
            raise InvalidStateTransitionError(
                f"Cannot transition order from {current.value} to {target.value}"
            )
        return target
