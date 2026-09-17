import unittest
from order_processor import OrderProcessor, OrderItem, OrderStatus, InvalidStateTransitionError

class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = OrderProcessor()

    # Happy Path & Tiered Discounts
    def test_empty_items_returns_zero(self):
        total = self.processor.calculate_total([])
        self.assertEqual(total, 0.0)

    def test_under_50_no_discount(self):
        # subtotal: 40.0, tax: 8% -> 43.20
        items = [OrderItem(sku="A", unit_price=20.0, quantity=2)]
        total = self.processor.calculate_total(items)
        self.assertEqual(total, 43.20)

    def test_between_50_and_100_tier_discount_5_percent(self):
        # subtotal: 60.0, 5% off -> 57.0, tax 8% -> 61.56
        items = [OrderItem(sku="B", unit_price=30.0, quantity=2)]
        total = self.processor.calculate_total(items)
        self.assertEqual(total, 61.56)

    def test_100_and_above_tier_discount_10_percent(self):
        # subtotal: 100.0, 10% off -> 90.0, tax 8% -> 97.20
        items = [OrderItem(sku="C", unit_price=100.0, quantity=1)]
        total = self.processor.calculate_total(items)
        self.assertEqual(total, 97.20)

    def test_vip_discount_applied_multiplicatively(self):
        # subtotal: 100.0, 10% off -> 90.0, VIP 5% off -> 85.50, tax 8% -> 92.34
        items = [OrderItem(sku="C", unit_price=100.0, quantity=1)]
        total = self.processor.calculate_total(items, is_vip=True)
        self.assertEqual(total, 92.34)

    # State Machine & Invariants
    def test_valid_state_transitions(self):
        self.assertEqual(
            self.processor.transition_state(OrderStatus.PENDING, OrderStatus.PAID),
            OrderStatus.PAID
        )
        self.assertEqual(
            self.processor.transition_state(OrderStatus.PENDING, OrderStatus.CANCELLED),
            OrderStatus.CANCELLED
        )

    def test_invalid_state_transitions_raise_error(self):
        with self.assertRaises(InvalidStateTransitionError):
            self.processor.transition_state(OrderStatus.PAID, OrderStatus.CANCELLED)

        with self.assertRaises(InvalidStateTransitionError):
            self.processor.transition_state(OrderStatus.CANCELLED, OrderStatus.PAID)

    # Invariants & Edge Cases
    def test_negative_unit_price_rejected(self):
        with self.assertRaises(ValueError):
            OrderItem(sku="ERR", unit_price=-5.0, quantity=1)

    def test_zero_or_negative_quantity_rejected(self):
        with self.assertRaises(ValueError):
            OrderItem(sku="ERR", unit_price=10.0, quantity=0)

if __name__ == "__main__":
    unittest.main()
