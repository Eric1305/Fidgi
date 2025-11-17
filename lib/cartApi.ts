const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface CartItem {
  id: number;
  item_id: number;
  quantity: number;
  item: {
    name: string;
    price: number;
    image: string;
    available_quantity: number;
  };
  in_stock: boolean;
  max_available: number;
}

export async function addToCart(token: string, itemId: number, quantity: number = 1) {
  const response = await fetch(`${API_URL}/cart/items`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item_id: itemId, quantity }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to add to cart");
  }

  return response.json();
}

export async function getCart(token: string): Promise<CartItem[]> {
  const response = await fetch(`${API_URL}/cart`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch cart");
  }

  return response.json();
}

export async function updateCartItem(token: string, cartItemId: number, quantity: number) {
  const response = await fetch(`${API_URL}/cart/items/${cartItemId}`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ quantity }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to update cart");
  }

  return response.json();
}

export async function removeFromCart(token: string, cartItemId: number) {
  const response = await fetch(`${API_URL}/cart/items/${cartItemId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to remove from cart");
  }

  return response.json();
}