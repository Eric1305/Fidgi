"use client";

import React from "react";
import { useShoppingCart } from "@/app/context/CartContext";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetFooter,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { ShoppingCart } from "lucide-react";
import Link from "next/link";

export function CartDrawer() {
  const { isOpen, closeCart, cartQuantity } = useShoppingCart();

  return (
    <Sheet open={isOpen} onOpenChange={closeCart}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            <ShoppingCart className="h-5 w-5" />
            Shopping Cart ({cartQuantity})
          </SheetTitle>
        </SheetHeader>

        <div className="flex-1 py-4">
          {cartQuantity === 0 ? (
            <div className="flex h-full flex-col items-center justify-center text-center">
              <ShoppingCart className="h-16 w-16 text-muted-foreground mb-4" />
              <p className="text-muted-foreground">Your cart is empty</p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Cart items would go here */}
              <p className="text-sm text-muted-foreground">
                {cartQuantity} item(s) in your cart
              </p>
            </div>
          )}
        </div>

        <SheetFooter>
          <Link href="/cart" className="w-full" onClick={closeCart}>
            <Button className="w-full" size="lg">
              Checkout
            </Button>
          </Link>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
