# TDD + SDD Reference Implementations

This directory provides concrete, runnable demonstrations of the Test-Driven & Spec-Driven Development methodology in multiple languages:

## 1. Python Example (`python_example/`)
- **Domain**: E-commerce Order Processor with tiered discounts, VIP perks, and strict state machine transitions.
- **Specification**: [spec.md](./python_example/spec.md)
- **Implementation**: [order_processor.py](./python_example/order_processor.py)
- **Tests**: [test_order_processor.py](./python_example/test_order_processor.py)
- **Run Command**:
  ```bash
  python -m unittest discover -s .agents/skills/tdd-sdd/examples/python_example
  ```

## 2. JavaScript / TypeScript Example (`typescript_example/`)
- **Domain**: Shopping Cart Discount Engine with percentage and flat coupons, shipping waivers, and date expirations.
- **Specification**: [spec.md](./typescript_example/spec.md)
- **Implementation**: [cart_discount.js](./typescript_example/cart_discount.js)
- **Tests**: [cart_discount.test.js](./typescript_example/cart_discount.test.js)
- **Run Command**:
  ```bash
  node --test .agents/skills/tdd-sdd/examples/typescript_example/cart_discount.test.js
  ```
