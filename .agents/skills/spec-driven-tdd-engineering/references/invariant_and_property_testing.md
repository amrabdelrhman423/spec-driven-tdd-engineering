# Invariant & Property-Based Testing

## 1. What is an Invariant?

An invariant is a condition or truth about a system that must always hold across all valid states and operations.

Examples of domain invariants:
- **Banking**: `account.balance >= 0` (or `account.balance + overdraft_limit >= 0`).
- **E-Commerce**: `order.total == sum(item.price * item.quantity for item in order.items) - order.discount + order.tax`.
- **Cache**: `cache.size <= cache.capacity`.
- **Sorting**: For any list `L`, `sorted(L)` contains identical elements with `L[i] <= L[i+1]` for all `i`.

---

## 2. Testing Invariants in TDD

In addition to individual unit example tests, write invariant assertions:

```python
def test_cart_invariants(cart):
    # Perform operations
    cart.add_item("item-1", 10.0, 2)
    cart.apply_discount(5.0)
    
    # Assert system invariant
    assert cart.total_price >= 0, "Cart total cannot be negative"
    assert cart.item_count == sum(i.quantity for i in cart.items)
```

---

## 3. Property-Based Testing Principles

Instead of testing hardcoded inputs `(2, 3) -> 5`, property-based testing generates hundreds of randomized inputs to test fundamental properties:

- **Roundtrip / Inverse**: `deserialize(serialize(x)) == x`
- **Idempotence**: `clean(clean(text)) == clean(text)`
- **Commutativity**: `add(a, b) == add(b, a)`
- **Metamorphic relations**: If input array grows by one positive element, the sum must strictly increase.

Tools to utilize:
- **Python**: `hypothesis`
- **TypeScript/JavaScript**: `fast-check`
- **Go**: `testing/quick`
