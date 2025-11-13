"use client";

import { ProductCard } from "@/components/product-card";

const products = [
  {
    id: 1,
    name: "Infinity Cube",
    price: 24.99,
    image: "/img/metallic-infinity-cube-fidget-toy.jpg",
    category: "Cubes",
    description: "Premium aluminum infinity cube with smooth rotation",
  },
  {
    id: 2,
    name: "Magnetic Spinner",
    price: 19.99,
    image: "/img/colorful-magnetic-fidget-spinner.jpg",
    category: "Spinners",
    description: "High-speed magnetic bearing spinner",
  },
  {
    id: 3,
    name: "Sensory Ring Set",
    price: 14.99,
    image: "/img/colorful-fidget-rings-set.jpg",
    category: "Rings",
    description: "Silicone textured rings for tactile stimulation",
  },
  {
    id: 4,
    name: "Fidget Pad Pro",
    price: 29.99,
    image: "/img/multi-function-fidget-pad-with-buttons.jpg",
    category: "Pads",
    description: "Multi-function pad with buttons, switches, and sliders",
  },
  {
    id: 5,
    name: "Mesh Marble",
    price: 16.99,
    image: "/img/mesh-and-marble-fidget-toy.jpg",
    category: "Marbles",
    description: "Stainless steel mesh with satisfying marble movement",
  },
  {
    id: 6,
    name: "Chain Links",
    price: 12.99,
    image: "/img/colorful-chain-link-fidget-toy.jpg",
    category: "Chains",
    description: "Interlocking chain links with smooth motion",
  },
  {
    id: 7,
    name: "Pop Bubble Keychain",
    price: 9.99,
    image: "/img/pop-bubble-fidget-keychain.jpg",
    category: "Keychains",
    description: "Portable pop bubble sensory keychain",
  },
  {
    id: 8,
    name: "Roller Chain",
    price: 21.99,
    image: "/img/metal-roller-chain-fidget-toy.jpg",
    category: "Chains",
    description: "Silent roller chain with premium finish",
  },
];

export function ProductGrid() {
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
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}
