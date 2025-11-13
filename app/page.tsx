import HomePage from "@/components/homepage";
import { ProductGrid } from "@/components/product-grid";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <div>
      <HomePage />
      <ProductGrid />
      <Footer />
    </div>
  );
}
