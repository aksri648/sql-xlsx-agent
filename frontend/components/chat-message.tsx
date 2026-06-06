import { Message, ChartConfig } from "@/types";
import { CodeBlock } from "./code-block";
import { ChartComponent } from "./chart";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import ReactMarkdown from "react-markdown";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <Card
        className={`max-w-[80%] p-4 ${
          isUser
            ? "bg-primary text-primary-foreground border-primary"
            : "bg-card"
        }`}
      >
        <div className="prose prose-sm max-w-none dark:prose-invert">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {message.insights && message.insights.length > 0 && (
          <div className="mt-4 pt-4 border-t border-current/20">
            <h4 className="text-sm font-semibold mb-2">Key Insights</h4>
            <ul className="text-sm space-y-1">
              {message.insights.map((insight, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="mt-1">•</span>
                  <span>{insight}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {message.chart && (
          <div className="mt-4">
            <ChartComponent config={message.chart} />
          </div>
        )}

        {message.sql && (
          <div className="mt-4">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="outline">SQL</Badge>
              <h4 className="text-sm font-semibold">Generated Query</h4>
            </div>
            <CodeBlock code={message.sql} language="sql" />
          </div>
        )}

        {message.pandas && (
          <div className="mt-4">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="outline">Pandas</Badge>
              <h4 className="text-sm font-semibold">Generated Code</h4>
            </div>
            <CodeBlock code={message.pandas} language="python" />
          </div>
        )}
      </Card>
    </div>
  );
}