const { test, describe } = require("node:test");
const assert = require("node:assert/strict");
const { calculateCart, InvalidCouponError, CouponExpiredError } = require("./cart_discount");

describe("Cart Discount Engine (TDD Suite)", () => {
  test("empty cart returns zeros", () => {
    const result = calculateCart({ items: [] });
    assert.deepEqual(result, {
      subtotal: 0,
      discount: 0,
      shipping: 0,
      total: 0
    });
  });

  test("calculates subtotal with standard shipping under $100", () => {
    const items = [{ id: "1", name: "Shirt", price: 25.0, quantity: 2 }];
    const result = calculateCart({ items });
    assert.equal(result.subtotal, 50.0);
    assert.equal(result.discount, 0);
    assert.equal(result.shipping, 5.0);
    assert.equal(result.total, 55.0);
  });

  test("applies free shipping for orders >= $100", () => {
    const items = [{ id: "2", name: "Jacket", price: 120.0, quantity: 1 }];
    const result = calculateCart({ items });
    assert.equal(result.subtotal, 120.0);
    assert.equal(result.shipping, 0.0);
    assert.equal(result.total, 120.0);
  });

  test("applies percentage coupon SUMMER20", () => {
    const items = [{ id: "1", name: "Book", price: 50.0, quantity: 1 }];
    const result = calculateCart({
      items,
      couponCode: "SUMMER20",
      now: new Date("2026-06-01")
    });
    assert.equal(result.discount, 10.0); // 20% of 50
    assert.equal(result.total, 45.0); // (50 - 10) + 5 shipping
  });

  test("rejects unknown coupon code with InvalidCouponError", () => {
    assert.throws(
      () => calculateCart({ items: [], couponCode: "BOGUS" }),
      InvalidCouponError
    );
  });

  test("rejects expired coupon with CouponExpiredError", () => {
    assert.throws(
      () =>
        calculateCart({
          items: [{ id: "1", name: "Pen", price: 10, quantity: 1 }],
          couponCode: "SUMMER20",
          now: new Date("2027-01-01")
        }),
      CouponExpiredError
    );
  });

  test("enforces domain invariant: negative price throws", () => {
    assert.throws(() =>
      calculateCart({
        items: [{ id: "err", name: "Bad", price: -10, quantity: 1 }]
      })
    );
  });
});
