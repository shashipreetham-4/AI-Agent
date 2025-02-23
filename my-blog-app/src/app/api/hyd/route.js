import { connectToDB } from "@/lib/mongodb";
import mongoose from "mongoose";

// Define Schema for Hyderabad Articles
const hydSchema = new mongoose.Schema({
  title: String,
  title_hi: String,
  date: String,
  keywords: [String],
  keywords_hi: [String],
  meta_description: String,
  meta_description_hi: String,
  text: String,
  text_hi: String,
  summary: String,
  summary_hi: String,
  topic: String,
  createdAt: { type: Date, default: Date.now },
});

// Prevent re-registering model
const HydArticle = mongoose.models.HydArticle || mongoose.model("HydArticle", hydSchema, "hyd");

export async function GET(req) {
  await connectToDB();

  const { searchParams } = new URL(req.url);
  const page = parseInt(searchParams.get("page") || "1", 10);
  const perPage = 5;

  const articles = await HydArticle.find()
    .sort({ createdAt: -1 })
    .skip((page - 1) * perPage)
    .limit(perPage);

  return Response.json(articles);
}