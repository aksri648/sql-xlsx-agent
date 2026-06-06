export interface ChartConfig {
  chart_type: string;
  x_axis: string;
  y_axis: string;
  title?: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  insights?: string[];
  chart?: ChartConfig;
  sql?: string;
  pandas?: string;
}

export interface ChatResponse {
  answer: string;
  insights: string[];
  chart?: ChartConfig;
  generated_sql?: string;
  generated_pandas?: string;
  sources: string[];
  follow_up_questions: string[];
  session_id: string;
}

export interface Dataset {
  id: string;
  name: string;
  source_type: string;
  row_count: number;
  column_count: number;
  columns: Array<{
    name: string;
    dtype: string;
    [key: string]: any;
  }>;
}