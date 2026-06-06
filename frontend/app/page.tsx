import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Database, MessageSquare, FileSpreadsheet, BarChart3 } from "lucide-react";

const features = [
  {
    icon: MessageSquare,
    title: "Natural Language Chat",
    description: "Ask questions in plain English and get answers, charts, and insights.",
  },
  {
    icon: FileSpreadsheet,
    title: "File Upload",
    description: "Upload CSV and Excel files for instant analysis.",
  },
  {
    icon: Database,
    title: "Database Connectors",
    description: "Connect to PostgreSQL, MySQL, or SQLite databases.",
  },
  {
    icon: BarChart3,
    title: "AI-Powered Insights",
    description: "Get executive summaries, key findings, and recommendations.",
  },
];

export default function Home() {
  return (
    <main className="container py-16">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-chart-2 bg-clip-text text-transparent">
          AI Data Analyst Platform
        </h1>
        <p className="text-xl text-muted-foreground mb-8">
          Upload datasets, connect databases, and query data using natural language.
          Powered by LangGraph, Groq AI, ChromaDB, and Tavily.
        </p>
        <div className="flex gap-4 justify-center">
          <Button asChild size="lg">
            <Link href="/chat">Start Chatting</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/datasets">Upload Dataset</Link>
          </Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {features.map((feature) => (
          <Card key={feature.title}>
            <CardHeader>
              <feature.icon className="h-8 w-8 text-primary mb-2" />
              <CardTitle className="text-lg">{feature.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>{feature.description}</CardDescription>
            </CardContent>
          </Card>
        ))}
      </div>
    </main>
  );
}