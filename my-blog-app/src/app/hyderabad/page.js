"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation"; 

export default function HyderabadBlogs() {
  const [blogs, setBlogs] = useState([]);
  const [page, setPage] = useState(1);
  const router = useRouter();

  const fetchBlogs = async () => {
    try {
      const response = await axios.get(`/api/hyd?page=${page}`);
      setBlogs(response.data);
    } catch (error) {
      console.error("Error fetching Hyderabad blogs:", error);
    }
  };

  useEffect(() => {
    fetchBlogs();
  }, [page]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Hyderabad News</h1>

      {/* Back to Home */}
      <button
        className="px-4 py-2 bg-gray-500 text-white rounded mb-4 mr-4"
        onClick={() => router.push("/")}
      >
        Back to Home
      </button>

      {/* Go to Hindi Version */}
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded mb-4"
        onClick={() => router.push("/hyderabad/hi")}
      >
        हिंदी संस्करण देखें
      </button>

      <div className="space-y-6">
        {blogs.map((blog) => (
          <div key={blog._id} className="border p-4 rounded-lg shadow-lg bg-white">
            <h2 className="text-2xl font-semibold">{blog.title}</h2>
            <p className="text-sm text-gray-500">🗓️ {blog.date}</p>
            <p className="text-gray-700 my-2">{blog.meta_description}</p>
            <p className="text-gray-900">{blog.text}</p>
            <p className="text-sm text-blue-600 mt-2">📝 Keywords: {blog.keywords.join(", ")}</p>
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="mt-6 flex justify-between">
        <button
          className="px-4 py-2 bg-gray-800 text-white rounded disabled:opacity-50"
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <button
          className="px-4 py-2 bg-gray-800 text-white rounded"
          onClick={() => setPage((prev) => prev + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}