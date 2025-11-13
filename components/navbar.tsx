// components/Navbar.tsx
import React, { FC } from "react";
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/nextjs";
import { ShoppingCart } from "lucide-react";
import { Search } from "lucide-react";

interface NavbarProps {
  cartItemCount?: number;
}

const Navbar: FC<NavbarProps> = ({ cartItemCount = 0 }) => {
  return (
    <nav className="bg-white shadow-md sticky top-0 z-50 flex justify-between items-center px-4 h-16 border-b-gray-600 ">
      {/* Logo */}
      <div className="text-2xl font-bold text-gray-800">Fidgi</div>

      {/* Auth + Cart */}
      <div className="flex items-center space-x-4">
        <div className="relative">
          <input
            type="text"
            placeholder="Search products..."
            className="border rounded-md pl-10 pr-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        </div>

        <a href="/cart" className="relative">
          <ShoppingCart className="h-6 w-6 text-gray-700 hover:text-gray-900" />
          {cartItemCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full text-xs w-5 h-5 flex items-center justify-center">
              {cartItemCount}
            </span>
          )}
        </a>

        {/* Clerk Auth Buttons */}
        <SignedOut>
          <SignInButton>
            <button className="bg-black text-white rounded-md px-3 py-1 text-sm">
              Sign In
            </button>
          </SignInButton>
          <SignUpButton>
            <button className="bg-white text-black border border-black rounded-md px-3 py-1 text-sm">
              Sign Up
            </button>
          </SignUpButton>
        </SignedOut>
        <SignedIn>
          <UserButton />
        </SignedIn>
      </div>
    </nav>
  );
};

export default Navbar;
