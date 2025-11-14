"use client";

import { ProductCard } from "@/components/product-card";
import { useEffect, useState } from "react";

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
  description: string;
}

interface ProductGridProps {
  searchTerm: string; 
}

export function ProductGrid({ searchTerm }: ProductGridProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  
  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch(`${API_URL}/items`);
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [API_URL]);

  if (loading) {
    return <div className="text-center py-16">Loading products...</div>;
  }

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section id="products" className="py-16 md:py-24 mt-10">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-balance">
            Our Collection
          </h2>
          <p className="text-lg text-muted-foreground text-pretty max-w-2xl mx-auto">
            Carefully curated fidget toys designed for every preference. From
            silent spinners to tactile cubes.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}