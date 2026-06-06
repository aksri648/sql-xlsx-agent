"use client";

import { useState } from "react";
import { Settings, Moon, Sun, Key, Database } from "lucide-react";

export default function SettingsPage() {
  const [darkMode, setDarkMode] = useState(false);
  const [apiKeys, setApiKeys] = useState({
    groq: "",
    chroma: "",
    tavily: "",
  });

  return (
    <div className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Settings</h1>

      <div className="max-w-2xl space-y-6">
        <div className="border rounded-lg p-6 bg-card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Appearance
          </h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Dark Mode</p>
              <p className="text-sm text-muted-foreground">Toggle dark mode theme</p>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg border hover:bg-accent"
            >
              {darkMode ? (
                <Moon className="h-5 w-5" />
              ) : (
                <Sun className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>

        <div className="border rounded-lg p-6 bg-card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Key className="h-5 w-5" />
            API Keys
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Groq API Key</label>
              <input
                type="password"
                value={apiKeys.groq}
                onChange={(e) => setApiKeys({ ...apiKeys, groq: e.target.value })}
                placeholder="gsk_..."
                className="w-full px-3 py-2 border rounded-lg bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Chroma API Key</label>
              <input
                type="password"
                value={apiKeys.chroma}
                onChange={(e) => setApiKeys({ ...apiKeys, chroma: e.target.value })}
                placeholder="..."
                className="w-full px-3 py-2 border rounded-lg bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Tavily API Key</label>
              <input
                type="password"
                value={apiKeys.tavily}
                onChange={(e) => setApiKeys({ ...apiKeys, tavily: e.target.value })}
                placeholder="..."
                className="w-full px-3 py-2 border rounded-lg bg-background"
              />
            </div>
            <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90">
              Save Changes
            </button>
          </div>
        </div>

        <div className="border rounded-lg p-6 bg-card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Database className="h-5 w-5" />
            Model Configuration
          </h2>
          <div>
            <label className="block text-sm font-medium mb-1">Default Model</label>
            <select className="w-full px-3 py-2 border rounded-lg bg-background">
              <option value="qwen/qwen3-32b">Qwen 3 32B</option>
              <option value="llama-3.3-70b">Llama 3.3 70B</option>
              <option value="mixtral-8x7b">Mixtral 8x7B</option>
            </select>
            <p className="text-sm text-muted-foreground mt-1">
              Configure which AI model to use for analysis
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}