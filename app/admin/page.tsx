"use client";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { ProductCard } from "@/components/product-card";
import { useEffect, useState } from "react";
import Navbar from "@/components/navbar";
import { ItemCard } from "@/components/item-card";

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
  description: string;
  quantity: number;
}

interface ProductGridProps {
  searchTerm: string; 
}

interface Order {
    id: number;
    user_id: number;
    subtotal: number;
    discount: number;
    tax: number;
    total: number;
    discount_code: string;
    stripe_payment_id: string
    status: string;
}


export default function Admin(){
    const [searchTerm, setSearchTerm] = useState("") 

    //const [items, setItems] = useState<Item[]>([]);

    

    return (
        // <div>
        //     <Navbar setSearchTerm={setSearchTerm}/>
        //     <ProductTable searchTerm={searchTerm}/>
        // </div>
        <div>
            <ItemTable>

            </ItemTable>
        </div>
    )
}

export function OrderTable(){
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState(true);
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    useEffect(() => {
        async function fetchOrders() {
        try {
            const response = await fetch(`${API_URL}/orders`);
            const data = await response.json();
            setOrders(data);
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        } finally {
            setLoading(false);
        }
    };

        fetchOrders();
    }, [API_URL]);

    if (loading) {
        return <div className="text-center py-16">Loading products...</div>;
    }

    //  const filteredOrders = orders.filter((order) =>
    //      order.created_at.toString());
    return(
    <section id="orders" className="py-16 md:py-24 mt-10">
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

        <div className="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-4 gap-6">
          {orders.map((order) => (
            <Card key={order.id}>
                <h3>
                    Order id: {order.id}
                </h3>
                <h3>
                    User id: {order.user_id}
                </h3>
                <h3>
                    Subtotal: {order.subtotal}
                </h3>
                <h3>
                    Discount: {order.discount}
                </h3>
                <h3>
                    Status: {order.status}
                </h3>
                
            </Card>
          ))}
        </div>
      </div>
    </section>
    )
}

export function ItemTable(){
    const [items, setItems] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    useEffect(() => {
        async function fetchItems() {
        try {
            const response = await fetch(`${API_URL}/items`);
            const data = await response.json();
            setItems(data);
        } catch (error) {
            console.error("Failed to fetch Items:", error);
        } finally {
            setLoading(false);
        }
    };

        fetchItems();
    }, [API_URL]);

    if (loading) {
        return <div className="text-center py-16">Loading products...</div>;
    }

    //  const filteredItems = Items.filter((Item) =>
    //      Item.created_at.toString());
    return(
    <section id="items" className="py-16 md:py-24 mt-10">
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

        <div className="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-4 gap-6">
          {items.map((item) => (
            <ItemCard key={item.id} item={item}>
                
            </ItemCard>
          ))}
        </div>
      </div>
    </section>
    )
}