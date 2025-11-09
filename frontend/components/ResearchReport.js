"use client";

export default function ResearchReport({ report }) {
  return (
    <section className="mt-6 bg-white shadow-sm rounded p-6">
      <h2 className="text-xl font-semibold mb-2">📋 Research Report</h2>
      <div className="prose max-w-none whitespace-pre-wrap">{report}</div>
    </section>
  );
}
