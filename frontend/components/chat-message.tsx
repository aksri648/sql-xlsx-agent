import { Message, ChartConfig } from "@/types";
import { CodeBlock } from "./code-block";
import { ChartComponent } from "./chart";
import ReactMarkdown from "react-markdown";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser ? "bg-primary text-primary-foreground" : "bg-card border"
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
            <h4 className="text-sm font-semibold mb-2">Generated SQL</h4>
            <CodeBlock code={message.sql} language="sql" />
          </div>
        )}

        {message.pandas && (
          <div className="mt-4">
            <h4 className="text-sm font-semibold mb-2">Generated Pandas</h4>
            <CodeBlock code={message.pandas} language="python" />
          </div>
        )}
      </div>
    </div>
  );
}