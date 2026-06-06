import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">AI Data Analyst Platform</h1>
      <p className="text-lg text-muted-foreground mb-8">
        Upload datasets, connect databases, and query data using natural language
      </p>
      <div className="flex gap-4">
        <Link
          href="/chat"
          className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
        >
          Start Chatting
        </Link>
        <Link
          href="/datasets"
          className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90"
        >
          View Datasets
        </Link>
      </div>
    </main>
  );
}