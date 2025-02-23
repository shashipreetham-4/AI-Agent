export default function BlogCard({ blog, language }) {
    return (
      <div className="border p-4 rounded-lg shadow-lg bg-white">
        <h2 className="text-2xl font-semibold">{language === "hi" ? blog.title_hi : blog.title}</h2>
        <p className="text-sm text-gray-500">🗓️ {blog.date}</p>
        <p className="text-gray-700 my-2">{language === "hi" ? blog.meta_description_hi : blog.meta_description}</p>
        <p className="text-gray-900">{language === "hi" ? blog.summary_hi : blog.summary}</p>
        <p className="text-sm text-blue-600 mt-2">📝 {language === "hi" ? "कीवर्ड्स" : "Keywords"}: {language === "hi" ? blog.keywords_hi.join(", ") : blog.keywords.join(", ")}</p>
      </div>
    );
  }