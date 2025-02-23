"use client";
import Blogs from "@/components/Blogs";
import { useRouter } from "next/navigation";

export default function HindiBlogs() {
  const router = useRouter();

  return (
    <div className="flex flex-col items-center">
      <div className="mt-4"> {/* Added margin to lower the button */}
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded"
          onClick={() => router.push("/")}
        >
          Back to English
        </button>
      </div>
      <Blogs language="hi" />
    </div>
  );
}