import React from "react";
export default function PaymentSuccess({
  searchParams,
}: {
  searchParams: Promise<{ amount?: string }>;
}) {
  const { amount } = React.use(searchParams);

  return (
    <main className="max-w-6xl mx-auto p-10 text-black text-center border m-10 rounded-md">
      <div className="mb-10">
        <h1 className="text-4xl font-extrabold mb-2">Thank you!</h1>
        <h2 className="text-2xl">Your order is complete</h2>

        <div className="bg-white p-2 rounded-md text-black-500 mt-5 text-4xl font-bold">
          ${amount}
        </div>
      </div>
    </main>
  );
}
