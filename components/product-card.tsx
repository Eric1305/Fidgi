"use client";

import Image from "next/image";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ShoppingCart } from "lucide-react";

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
  description: string;
  quantity: number;
}

export function ProductCard({ product }: { product: Product }) {
  const isOutOfStock = product.quantity === 0;
  const isLowStock = product.quantity > 0 && product.quantity <= 5;

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
            src={product.image || "/placeholder.svg"}
            alt={product.name}
            fill
            className="object-cover transition-transform group-hover:scale-105"
          />
        </div>
        <div className="p-4 space-y-2">
          <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
            {product.category}
          </div>
          <h3 className="font-semibold text-lg text-balance">{product.name}</h3>
          <p className="text-sm text-muted-foreground line-clamp-2">
            {product.description}
          </p>
          <div className="pt-1">
            {isLowStock ? (
              <p className="text-sm font-semibold text-orange-600">
                Only {product.quantity} left in stock!
              </p>
            ) : (
              <p className="text-sm text-muted-foreground">
                {product.quantity} in stock
              </p>
            )}
          </div>
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-0 flex items-center justify-between">
        <span className="text-2xl font-bold">${product.price}</span>
        <Button size="sm" className="gap-2" disabled={isOutOfStock}>
          <ShoppingCart className="h-4 w-4" />
          {isOutOfStock ? "Out of Stock" : "Add"}
        </Button>
      </CardFooter>
    </Card>
  );
}