"use client";
import { useState } from "react";
import ResearchReport from "../components/ResearchReport";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleResearch = async () => {
    setError("");
    setReport("");
    if (!topic.trim()) {
      setError("Please enter a topic.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic })
      });
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || "Backend error");
      }
      const data = await res.json();
      setReport(data.report || "No report returned.");
    } catch (e) {
      setError(e.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <div className="w-full max-w-2xl">
        <label className="block text-sm font-medium text-gray-700 mb-2">Topic</label>
        <input
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="w-full border p-3 rounded shadow-sm"
          placeholder="e.g., 'AI trends 2026'"
        />
        <div className="flex gap-3 mt-4">
          <button
            onClick={handleResearch}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-60"
          >
            {loading ? "Researching..." : "Start Research"}
          </button>
          <button
            onClick={() => { setTopic(""); setReport(""); setError(""); }}
            className="bg-gray-200 px-4 py-2 rounded"
          >
            Reset
          </button>
        </div>

        {error && <p className="mt-4 text-red-600">{error}</p>}

        {report && <ResearchReport report={report} />}
      </div>
    </div>
  );
}

