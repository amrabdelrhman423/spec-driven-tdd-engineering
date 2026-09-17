# Specification: Shopping Cart Discount Engine

**Module**: `cart_discount.js`  
**Status**: APPROVED  

## 1. Domain Invariants
- Applied coupon discount can never exceed total eligible item price.
- Final cart total must never be negative.
- Expired coupons must throw `CouponExpiredError`.
- Unknown coupons must throw `InvalidCouponError`.

## 2. Discount Rules
- **Coupon 'SUMMER20'**: Gives 20% off eligible items.
- **Coupon 'FLAT15'**: Gives $15 off if subtotal is at least $50; otherwise ineligible.
- Shipping is $5.00 flat, waived for carts with net subtotal >= $100.

## 3. Interface Contract
```typescript
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CalculateCartOptions {
  items: CartItem[];
  couponCode?: string;
  now?: Date;
}

interface CartSummary {
  subtotal: number;
  discount: number;
  shipping: number;
  total: number;
}
```
