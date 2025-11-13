import Image from "next/image";

export default function HomePage() {
  return (
    <section>
      <div className="flex-row flex mt-6">
        <div className="flex-col flex px-4 w-1/2 gap-4">
          <div className="text-7xl font-bold">
            Find Your Focus with Premium Fidget Toys
          </div>
          <p className="text-gray-400 text-2xl">
            Discover tactile tools designed to enhance concentration, reduce
            stress, and keep your hands engaged. Each piece is crafted for
            comfort and durability.
          </p>
        </div>
        <div className="relative aspect-square w-2/3  lg:aspect-auto lg:h-[500px]">
          <Image
            src="/img/fidget_toys_multiple.jpg"
            alt="Fidget toys collection"
            fill
            className="object-cover rounded-2xl"
            priority
          />
        </div>
      </div>
    </section>
  );
}
