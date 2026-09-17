# SDE Reference Implementations

This directory provides concrete reference implementations demonstrating the SDE Core, Framework Profiles, TDD, and Spec-Driven Engineering across multiple technology ecosystems:

---

## 1. Flutter Example (`flutter_example/`)
- **Domain**: User Authentication (Login) feature.
- **Framework Profile**: `flutter` (Dart 3.x, `flutter_bloc` Cubit, `get_it` service locator).
- **Architecture**: Feature-First Clean Architecture (`lib/features/auth/`).
- **Artifacts**: [spec.md](./flutter_example/specs/spec.md), [plan.md](./flutter_example/specs/plan.md), [risk.md](./flutter_example/specs/risk.md), [impact.md](./flutter_example/specs/impact.md), [tasks.md](./flutter_example/specs/tasks.md), [verification.md](./flutter_example/specs/verification.md).
- **Implementation Guide**: [README.md](./flutter_example/README.md)

---

## 2. Python Example (`python_example/`)
- **Domain**: E-commerce Order Processor with tiered discounts, VIP perks, and strict state machine transitions.
- **Specification**: [spec.md](./python_example/spec.md)
- **Implementation**: [order_processor.py](./python_example/order_processor.py)
- **Tests**: [test_order_processor.py](./python_example/test_order_processor.py)
- **Run Command**:
  ```bash
  python -m unittest discover -s .agents/skills/spec-driven-tdd-engineering/examples/python_example
  ```

---

## 3. JavaScript / TypeScript Example (`typescript_example/`)
- **Domain**: Shopping Cart Discount Engine with percentage and flat coupons, shipping waivers, and date expirations.
- **Specification**: [spec.md](./typescript_example/spec.md)
- **Implementation**: [cart_discount.js](./typescript_example/cart_discount.js)
- **Tests**: [cart_discount.test.js](./typescript_example/cart_discount.test.js)
- **Run Command**:
  ```bash
  node --test .agents/skills/spec-driven-tdd-engineering/examples/typescript_example/cart_discount.test.js
  ```
