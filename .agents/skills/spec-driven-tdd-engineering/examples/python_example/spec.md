# Specification: Order Processor Module

**Status**: APPROVED  
**Module**: `order_processor.py`  

## 1. Domain Invariants
- `order.total_amount >= 0.0`
- An order can only transition from `PENDING` -> `PAID` or `CANCELLED`.
- Disallowed state transitions must raise an `InvalidStateTransitionError`.

## 2. Discount Rules
- Orders under $50 receive 0% discount.
- Orders between $50 and $99.99 receive 5% discount.
- Orders of $100 and above receive 10% discount.
- VIP customers receive an additional 5% off the post-tier discounted amount.

## 3. Tax Calculation
- Flat tax rate of 8% applied after discounts.

## 4. Contract Signatures
```python
from dataclasses import dataclass
from enum import Enum
from typing import List

class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

@dataclass
class OrderItem:
    sku: str
    unit_price: float
    quantity: int

class OrderProcessor:
    def calculate_total(self, items: List[OrderItem], is_vip: bool = False) -> float: ...
    def transition_state(self, current: OrderStatus, target: OrderStatus) -> OrderStatus: ...
```
