"use client";
import Link from "next/link";
import Blogs from "@/components/Blogs";

export default function HyderabadPageHindi() {
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">हैदराबाद ब्लॉग्स</h1>

      {/* Button to navigate back to English version */}
      <Link href="/hyderabad">
        <button className="px-4 py-2 bg-blue-600 text-white rounded mb-4">
          अंग्रेज़ी में देखें
        </button>
      </Link>

      {/* Fetch and display Hyderabad blogs in Hindi */}
      <Blogs collection="hyd" language="hi" />
    </div>
  );
}