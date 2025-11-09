import "../styles/globals.css";

export const metadata = {
  title: "Multi-Agent Research Assistant",
  description: "Research assistant powered by autonomous agents and Groq"
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">
        <div className="min-h-screen">
          <header className="bg-white shadow-sm">
            <div className="max-w-5xl mx-auto px-6 py-4">
              <h1 className="text-2xl font-semibold">🧠 Multi-Agent Research Assistant</h1>
            </div>
          </header>
          <main className="max-w-5xl mx-auto px-6 py-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
