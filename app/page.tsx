"use client";

import { useState } from "react";
import Navbar from "@/components/navbar";
import HomePage from "@/components/homepage";
import { ProductGrid } from "@/components/product-grid";
import { Footer } from "@/components/footer";

export default function Home() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div>
      <Navbar setSearchTerm={setSearchTerm} />
      <HomePage />
      <ProductGrid searchTerm={searchTerm} />
      <Footer />
    </div>
  );
}
