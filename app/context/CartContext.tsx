"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { addToCart as addToCartAPI, getCart, removeFromCart as removeFromCartAPI, updateCartItem, CartItem } from "@/lib/cartApi";

interface CartContextType {
  cartItems: CartItem[];
  cartQuantity: number;
  isOpen: boolean;
  openCart: () => void;
  closeCart: () => void;
  addToCart: (itemId: number, quantity?: number) => Promise<void>;
  removeFromCart: (cartItemId: number) => Promise<void>;
  updateQuantity: (cartItemId: number, quantity: number) => Promise<void>;
  refreshCart: () => Promise<void>;
  isLoading: boolean;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function useShoppingCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useShoppingCart must be used within CartProvider");
  }
  return context;
}

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { getToken, isSignedIn } = useAuth();

  const cartQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);

  // Load cart when user signs in
  useEffect(() => {
    if (isSignedIn) {
      refreshCart();
    }
  }, [isSignedIn]);

  const refreshCart = async () => {
    if (!isSignedIn) return;
    
    try {
      setIsLoading(true);
      const token = await getToken();
      if (!token) return;
      
      const items = await getCart(token);
      setCartItems(items);
    } catch (error) {
      console.error("Failed to load cart:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const addToCart = async (itemId: number, quantity: number = 1) => {
    if (!isSignedIn) {
      alert("Please sign in to add items to cart");
      return;
    }

    try {
      const token = await getToken();
      if (!token) return;

      await addToCartAPI(token, itemId, quantity);
      await refreshCart(); // Reload cart
      openCart(); // Open drawer to show item was added
    } catch (error: any) {
      alert(error.message || "Failed to add to cart");
      console.error("Add to cart error:", error);
    }
  };

  const removeFromCart = async (cartItemId: number) => {
    try {
      const token = await getToken();
      if (!token) return;

      await removeFromCartAPI(token, cartItemId);
      await refreshCart();
    } catch (error) {
      console.error("Remove from cart error:", error);
    }
  };

  const updateQuantity = async (cartItemId: number, quantity: number) => {
    if (quantity <= 0) {
      await removeFromCart(cartItemId);
      return;
    }

    try {
      const token = await getToken();
      if (!token) return;

      await updateCartItem(token, cartItemId, quantity);
      await refreshCart();
    } catch (error: any) {
      alert(error.message || "Failed to update quantity");
      console.error("Update quantity error:", error);
    }
  };

  const openCart = () => setIsOpen(true);
  const closeCart = () => setIsOpen(false);

  return (
    <CartContext.Provider
      value={{
        cartItems,
        cartQuantity,
        isOpen,
        openCart,
        closeCart,
        addToCart,
        removeFromCart,
        updateQuantity,
        refreshCart,
        isLoading,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}