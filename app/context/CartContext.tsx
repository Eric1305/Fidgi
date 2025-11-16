"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

interface CartContextType {
  isOpen: boolean;
  openCart: () => void;
  closeCart: () => void;
  cartQuantity: number;
  setCartQuantity: (quantity: number) => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const [cartQuantity, setCartQuantity] = useState(0);

  const openCart = () => setIsOpen(true);
  const closeCart = () => setIsOpen(false);

  return (
    <CartContext.Provider
      value={{
        isOpen,
        openCart,
        closeCart,
        cartQuantity,
        setCartQuantity,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useShoppingCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useShoppingCart must be used within a CartProvider");
  }
  return context;
}
