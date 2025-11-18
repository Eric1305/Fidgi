"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { CheckCircle2, Package, Heart, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import Navbar from "@/components/navbar";
import { useShoppingCart } from "@/app/context/CartContext";

export default function OrderConfirmationPage() {
  const { cartItems } = useShoppingCart();

  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.item.price * item.quantity,
    0
  );

  const shipping = 9.99;
  const total = subtotal + shipping;

  // Order Number
  const orderNumber =
    "ORD-" + Math.random().toString(36).substr(2, 9).toUpperCase();

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="container mx-auto px-4 py-8 md:py-12 max-w-3xl">
        {/* Success Header */}
        <div className="text-center mb-6 md:mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 md:w-20 md:h-20 rounded-full bg-blue-100 mb-4 md:mb-6 animate-in zoom-in duration-300">
            <CheckCircle2 className="w-8 h-8 md:w-10 md:h-10 text-blue-500" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2 md:mb-3">
            Order Complete!
          </h1>
          <p className="text-base md:text-lg text-gray-600 flex items-center justify-center gap-2 flex-wrap">
            <span>Thank you for your purchase</span>
            <Heart className="w-4 h-4 text-blue-500 fill-blue-500" />
          </p>
        </div>

        {/* Order Summary */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Package className="w-5 h-5 text-blue-500" />
              <h2 className="text-xl font-semibold text-gray-900">
                Order Summary
              </h2>
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            {/* Order Items */}
            <div className="space-y-3">
              {cartItems.map((cart) => (
                <div
                  key={cart.id}
                  className="flex justify-between items-start gap-3 py-3 border-b last:border-b-0 border-gray-200"
                >
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900">
                      {cart.item.name}
                    </p>
                    <p className="text-sm text-gray-600">
                      Qty: {cart.quantity}
                    </p>
                  </div>
                  <p className="font-semibold text-gray-900 whitespace-nowrap">
                    ${(cart.item.price * cart.quantity).toFixed(2)}
                  </p>
                </div>
              ))}
            </div>

            {/* Pricing Breakdown */}
            <div className="pt-3 space-y-2 border-t border-gray-200">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Subtotal</span>
                <span className="text-gray-900 font-medium">
                  ${subtotal.toFixed(2)}
                </span>
              </div>

              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Shipping</span>
                <span className="text-gray-900 font-medium">
                  ${shipping.toFixed(2)}
                </span>
              </div>

              <div className="flex justify-between text-lg font-bold pt-2 border-t border-gray-200">
                <span className="text-gray-900">Total</span>
                <span className="text-blue-600">${total.toFixed(2)}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Next Steps */}
        <Card className="mb-6 bg-blue-50 border-blue-200">
          <CardContent className="pt-1">
            <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-500" />
              What happens next?
            </h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">•</span>
                <span>
                  You'll receive a confirmation email shortly with your order
                  details
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">•</span>
                <span>Your items will be shipped within 1–2 business days</span>
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <Button asChild className="flex-1" size="lg">
            <Link href="/">Continue Shopping</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
