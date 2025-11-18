"use client";

import React from "react";
import Link from "next/link";
import { CheckCircle2, Package, Heart, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import Navbar from "@/components/navbar";

export default function OrderConfirmationPage() {
  // Mock order data - in real app this would come from URL params or API
  const orderItems = [
    { id: 1, name: "Premium Cotton T-Shirt", quantity: 2, price: 29.99 },
    { id: 2, name: "Vintage Denim Jacket", quantity: 1, price: 89.99 },
    { id: 3, name: "Classic Sneakers", quantity: 1, price: 79.99 },
  ];

  const subtotal = orderItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const shipping = 9.99;
  const total = subtotal + shipping;
  const orderNumber =
    "ORD-" + Math.random().toString(36).substr(2, 9).toUpperCase();

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar cartItemCount={0} />

      <div className="container mx-auto px-4 py-8 md:py-12 max-w-3xl">
        {/* Success Header */}
        <div className="text-center mb-6 md:mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 md:w-20 md:h-20 rounded-full bg-blue-100 mb-4 md:mb-6 animate-in zoom-in duration-300">
            <CheckCircle2 className="w-8 h-8 md:w-10 md:h-10 text-blue-500" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2 md:mb-3 text-balance">
            Order Complete!
          </h1>
          <p className="text-base md:text-lg text-gray-600 flex items-center justify-center gap-2 flex-wrap">
            <span>Thank you for your purchase</span>
            <Heart className="w-4 h-4 text-blue-500 inline-block fill-blue-500" />
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
              {orderItems.map((item) => (
                <div
                  key={item.id}
                  className="flex justify-between items-start gap-3 py-3 border-b last:border-b-0 border-gray-200"
                >
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 text-pretty">
                      {item.name}
                    </p>
                    <p className="text-sm text-gray-600">
                      Qty: {item.quantity}
                    </p>
                  </div>
                  <p className="font-semibold text-gray-900 whitespace-nowrap">
                    ${(item.price * item.quantity).toFixed(2)}
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
                <span>
                  Your items will be carefully packaged and shipped within 1-2
                  business days
                </span>
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <Button asChild className="flex-1" size="lg">
            <Link href="/">Continue Shopping</Link>
          </Button>
        </div>

        {/* Support Message */}
        <p className="text-center text-sm text-gray-600 mt-8">
          Need help? Contact our{" "}
          <Link
            href="/support"
            className="text-blue-600 hover:underline font-medium"
          >
            support team
          </Link>
        </p>
      </div>
    </div>
  );
}
