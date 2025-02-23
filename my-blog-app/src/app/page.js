"use client"; 

import Link from "next/link";
import { useRouter } from "next/navigation";
import Blogs from "@/components/Blogs";

export default function Home() {
  const router = useRouter(); 

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Latest Blogs</h1>

      {/* Translate to Hindi Button */}
      <Link href="/hi">
        <button className="px-4 py-2 bg-blue-600 text-white rounded mr-4">
          Translate to Hindi
        </button>
      </Link>

      {/* Hyderabad Button */}
      <button
        className="px-4 py-2 bg-green-600 text-white rounded"
        onClick={() => router.push("/hyderabad")}
      >
        Hyderabad
      </button>

      {/* Blog Component */}
      <Blogs language="en" />
    </div>
  );
}