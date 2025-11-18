"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import Image from "next/image";
import { useState } from "react";
import { Plus, Minus } from "lucide-react";

interface Item {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
  description: string;
  quantity: number;
}

export function ItemCard({ item }: { item: Item }) {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  
  const isOutOfStock = item.quantity === 0;
  const isLowStock = item.quantity > 0 && item.quantity <= 5;

  const addQuantity = async () =>{
    const response = await fetch(`${API_URL}/${item.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json" 
      },
      body: JSON.stringify({quantity: item.quantity + 1}),
      });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to update quantity!!!!!!!!!!!!!!");
    }
      return response.json();
      
    }

  const subQuantity = async () =>{
    item.quantity -= 1
  }

  return (
    <Card className="group overflow-hidden hover:shadow-lg transition-shadow">
      <CardContent className="p-0">
        <div className="relative aspect-square overflow-hidden bg-muted">
          {isOutOfStock && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-10">
              <span className="text-white font-bold text-lg">Out of Stock</span>
            </div>
          )}
          <Image
            src={item.image || "/placeholder.svg"}
            alt={item.name}
            fill
            className="object-cover transition-transform group-hover:scale-105"
          />
        </div>
        <div className="p-4 space-y-2">
          <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
            {item.category}
          </div>
          <h3 className="font-semibold text-lg text-balance">{item.name}</h3>
          <p className="text-sm text-muted-foreground line-clamp-2">
            {item.description}
          </p>
          <div className="pt-1">
            {isLowStock ? (
              <p className="text-sm font-semibold text-orange-600">
                Only {item.quantity} left in stock!
              </p>
            ) : (
              <p className="text-sm text-muted-foreground">
                {item.quantity} in stock
              </p>
            )}
          </div>
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-0 flex items-center justify-between">
        <span className="text-2xl font-bold">${item.price}</span>
        <Button 
          size="sm" 
          className="gap-2" 
          onClick={addQuantity}
        >
          <Plus className="h-4 w-4" />
        </Button>
        <Button
          size="sm"
          className="gap-2"
          disabled={item.quantity == 0}
          onClick={subQuantity}
          >
            <Minus className="h-4 w-4"/>
        </Button>
      </CardFooter>
    </Card>
  );
}

export async function AdjustQuantity(token: string, ){

}