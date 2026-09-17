class InvalidCouponError extends Error {
  constructor(message) {
    super(message);
    this.name = "InvalidCouponError";
  }
}

class CouponExpiredError extends Error {
  constructor(message) {
    super(message);
    this.name = "CouponExpiredError";
  }
}

const COUPONS = {
  SUMMER20: {
    type: "PERCENT",
    value: 0.20,
    expiresAt: new Date("2026-12-31T23:59:59Z")
  },
  FLAT15: {
    type: "FLAT",
    value: 15.0,
    minSubtotal: 50.0,
    expiresAt: new Date("2026-12-31T23:59:59Z")
  }
};

/**
 * Calculates cart summary based on items, coupons, and business rules.
 */
function calculateCart({ items = [], couponCode, now = new Date() } = {}) {
  const subtotal = items.reduce((sum, item) => {
    if (item.price < 0 || item.quantity <= 0) {
      throw new Error(`Invalid item price (${item.price}) or quantity (${item.quantity})`);
    }
    return sum + item.price * item.quantity;
  }, 0);

  let discount = 0;

  if (couponCode) {
    const coupon = COUPONS[couponCode.toUpperCase()];
    if (!coupon) {
      throw new InvalidCouponError(`Coupon '${couponCode}' does not exist`);
    }

    if (now > coupon.expiresAt) {
      throw new CouponExpiredError(`Coupon '${couponCode}' has expired`);
    }

    if (coupon.type === "PERCENT") {
      discount = subtotal * coupon.value;
    } else if (coupon.type === "FLAT") {
      if (subtotal >= (coupon.minSubtotal || 0)) {
        discount = Math.min(coupon.value, subtotal);
      }
    }
  }

  const netSubtotal = Math.max(0, subtotal - discount);
  const shipping = netSubtotal >= 100.0 || items.length === 0 ? 0.0 : 5.0;
  const total = Number((netSubtotal + shipping).toFixed(2));

  return {
    subtotal: Number(subtotal.toFixed(2)),
    discount: Number(discount.toFixed(2)),
    shipping: Number(shipping.toFixed(2)),
    total
  };
}

module.exports = {
  calculateCart,
  InvalidCouponError,
  CouponExpiredError
};
