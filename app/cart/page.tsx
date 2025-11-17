"use client";

import { useShoppingCart } from "@/app/context/CartContext";
import CheckoutPage from "@/components/CheckoutPage";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import convertToSubcurrency from "@/lib/convertToSubcurrency";
import { useAuth } from "@clerk/nextjs";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { Minus, Plus, Trash2 } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

if (process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY === undefined) {
  throw new Error("NEXT_PUBLIC_STRIPE_PUBLIC_KEY is not defined");
}

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY);
const TAX_RATE = 0.0825; // 8.25%
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Cart() {
  const { cartItems, updateQuantity, removeFromCart, isLoading } = useShoppingCart();
  const { getToken } = useAuth();
  const [discountCode, setDiscountCode] = useState("");
  const [appliedDiscount, setAppliedDiscount] = useState<{
    code: string;
    percentage: number;
  } | null>(null);
  const [discountError, setDiscountError] = useState("");
  const [isApplyingDiscount, setIsApplyingDiscount] = useState(false);

  // Calculate totals
  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.item.price * item.quantity,
    0
  );
  
  const discountAmount = appliedDiscount 
    ? subtotal * (appliedDiscount.percentage / 100)
    : 0;
  
  const afterDiscount = subtotal - discountAmount;
  const tax = afterDiscount * TAX_RATE;
  const total = afterDiscount + tax;

  const applyDiscountCode = async () => {
    if (!discountCode.trim()) {
      setDiscountError("Please enter a discount code");
      return;
    }

    setIsApplyingDiscount(true);
    setDiscountError("");

    try {
      const token = await getToken();
      if (!token) return;

      const response = await fetch(`${API_URL}/discount/${discountCode}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        setDiscountError(error.detail || "Invalid discount code");
        setAppliedDiscount(null);
        return;
      }

      const discount = await response.json();
      setAppliedDiscount({
        code: discount.code,
        percentage: discount.discount_percentage,
      });
      setDiscountError("");
    } catch (error) {
      setDiscountError("Failed to apply discount code");
      setAppliedDiscount(null);
    } finally {
      setIsApplyingDiscount(false);
    }
  };

  const removeDiscount = () => {
    setAppliedDiscount(null);
    setDiscountCode("");
    setDiscountError("");
  };

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto p-10 text-center">
        <p className="text-gray-600">Loading cart...</p>
      </div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="max-w-6xl mx-auto p-10 text-center">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-6">
          Your Cart is Empty
        </h1>
        <p className="text-gray-600 mb-8">
          Add some items to your cart to get started!
        </p>
        <Button asChild>
          <a href="/">Continue Shopping</a>
        </Button>
      </div>
    );
  }

  return (
    <section className="max-w-6xl mx-auto p-10">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-8">
        Shopping Cart
      </h1>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="md:col-span-2 space-y-4">
          {cartItems.map((item) => (
            <div
              key={item.id}
              className="flex gap-4 border rounded-lg p-4 bg-white"
            >
              <div className="relative w-24 h-24 flex-shrink-0">
                <Image
                  src={item.item.image}
                  alt={item.item.name}
                  fill
                  className="object-cover rounded"
                />
              </div>

              <div className="flex-1">
                <h3 className="font-semibold text-lg">{item.item.name}</h3>
                <p className="text-gray-600">${item.item.price.toFixed(2)}</p>

                {!item.in_stock && (
                  <p className="text-red-600 text-sm mt-1">
                    Only {item.max_available} available
                  </p>
                )}

                <div className="flex items-center gap-2 mt-3">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <span className="w-12 text-center">{item.quantity}</span>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    disabled={item.quantity >= item.max_available}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="ml-auto text-red-600"
                    onClick={() => removeFromCart(item.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div className="text-right">
                <p className="font-semibold text-lg">
                  ${(item.item.price * item.quantity).toFixed(2)}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary */}
        <div className="space-y-6">
          <div className="border rounded-lg p-6 bg-white">
            <h2 className="text-xl font-bold mb-4">Order Summary</h2>

            {/* Discount Code */}
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">
                Discount Code
              </label>
              {appliedDiscount ? (
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <div>
                    <p className="font-semibold text-green-700">
                      {appliedDiscount.code}
                    </p>
                    <p className="text-sm text-green-600">
                      {appliedDiscount.percentage}% off
                    </p>
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={removeDiscount}
                    className="text-red-600"
                  >
                    Remove
                  </Button>
                </div>
              ) : (
                <>
                  <div className="flex gap-2">
                    <Input
                      type="text"
                      placeholder="Enter code"
                      value={discountCode}
                      onChange={(e) => setDiscountCode(e.target.value.toUpperCase())}
                      onKeyPress={(e) => e.key === "Enter" && applyDiscountCode()}
                    />
                    <Button
                      onClick={applyDiscountCode}
                      disabled={isApplyingDiscount}
                    >
                      {isApplyingDiscount ? "..." : "Apply"}
                    </Button>
                  </div>
                  {discountError && (
                    <p className="text-red-600 text-sm mt-1">{discountError}</p>
                  )}
                </>
              )}
            </div>

            {/* Price Breakdown */}
            <div className="space-y-2 border-t pt-4">
              <div className="flex justify-between text-gray-600">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>

              {appliedDiscount && (
                <div className="flex justify-between text-green-600">
                  <span>Discount ({appliedDiscount.percentage}%)</span>
                  <span>-${discountAmount.toFixed(2)}</span>
                </div>
              )}

              <div className="flex justify-between text-gray-600">
                <span>Tax (8.25%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>

              <div className="flex justify-between text-xl font-bold border-t pt-2">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>
          </div>

          {/* Checkout */}
          <div className="border rounded-lg p-6 bg-white">
            <h2 className="text-xl font-bold mb-4">Payment</h2>
            <Elements
              stripe={stripePromise}
              options={{
                mode: "payment",
                amount: convertToSubcurrency(total),
                currency: "usd",
              }}
            >
              <CheckoutPage 
                amount={total} 
                cartItems={cartItems}
                discountCode={appliedDiscount?.code}
              />
            </Elements>
          </div>
        </div>
      </div>
    </section>
  );
}