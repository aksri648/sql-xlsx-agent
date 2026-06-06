"use client";

import { useState } from "react";
import { Key, Database as DatabaseIcon } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  const [apiKeys, setApiKeys] = useState({
    groq: "",
    chroma: "",
    tavily: "",
  });

  const models = [
    { value: "qwen/qwen3-32b", label: "Qwen 3 32B" },
    { value: "llama-3.3-70b", label: "Llama 3.3 70B" },
    { value: "mixtral-8x7b", label: "Mixtral 8x7B" },
  ];

  return (
    <div className="container py-8">
      <h1 className="text-3xl font-bold mb-8">Settings</h1>

      <div className="max-w-2xl space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>API Keys</CardTitle>
            <CardDescription>Configure your AI service API keys</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="groq">
                <Key className="inline h-3 w-3 mr-1" />
                Groq API Key
              </Label>
              <Input
                id="groq"
                type="password"
                value={apiKeys.groq}
                onChange={(e) => setApiKeys({ ...apiKeys, groq: e.target.value })}
                placeholder="gsk_..."
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="chroma">Chroma API Key</Label>
              <Input
                id="chroma"
                type="password"
                value={apiKeys.chroma}
                onChange={(e) => setApiKeys({ ...apiKeys, chroma: e.target.value })}
                placeholder="ck-..."
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="tavily">Tavily API Key</Label>
              <Input
                id="tavily"
                type="password"
                value={apiKeys.tavily}
                onChange={(e) => setApiKeys({ ...apiKeys, tavily: e.target.value })}
                placeholder="tvly-..."
              />
            </div>
            <Button>Save Changes</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>
              <DatabaseIcon className="inline h-4 w-4 mr-2" />
              Model Configuration
            </CardTitle>
            <CardDescription>Choose which AI model to use for analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Label htmlFor="model">Default Model</Label>
              <select
                id="model"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                defaultValue="qwen/qwen3-32b"
              >
                {models.map((model) => (
                  <option key={model.value} value={model.value}>
                    {model.label}
                  </option>
                ))}
              </select>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}