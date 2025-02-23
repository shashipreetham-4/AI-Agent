"use client"; 

import { useEffect, useState } from "react";
import axios from "axios";
import BlogCard from "./BlogCard";

export default function Blogs({ language }) {
  const [blogs, setBlogs] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchBlogs();
  }, [page]); 

  const fetchBlogs = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/blogs?page=${page}`);
      setBlogs(response.data);
    } catch (error) {
      console.error("Error fetching blogs:", error);
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">{language === "hi" ? "नवीनतम ब्लॉग्स" : "Telangana"}</h1>
      
      {loading && <p>Loading...</p>}
      {blogs.length === 0 && !loading && <p>No blogs found.</p>}

      <div className="space-y-6">
        {blogs.map((blog) => (
          <BlogCard key={blog._id} blog={blog} language={language} />
        ))}
      </div>

      {/* Pagination Controls */}
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