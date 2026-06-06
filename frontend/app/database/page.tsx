"use client";

import { useState } from "react";
import { Database, Plus, Trash2, CheckCircle, XCircle } from "lucide-react";

type DatabaseConnection = {
  id: string;
  type: string;
  alias: string;
  status: "connected" | "disconnected";
};

export default function DatabasePage() {
  const [connections, setConnections] = useState<DatabaseConnection[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    type: "postgresql",
    connectionString: "",
    alias: "",
  });
  const [testing, setTesting] = useState(false);

  const handleConnect = async () => {
    setTesting(true);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    try {
      const response = await fetch(`${apiUrl}/database/connect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setConnections((prev) => [
          ...prev,
          {
            id: Date.now().toString(),
            type: formData.type,
            alias: formData.alias || formData.type,
            status: "connected",
          },
        ]);
        setShowForm(false);
        setFormData({ type: "postgresql", connectionString: "", alias: "" });
      }
    } catch (error) {
      console.error("Connection failed:", error);
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Database Connections</h1>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
        >
          <Plus className="h-4 w-4" />
          Add Connection
        </button>
      </div>

      {showForm && (
        <div className="border rounded-lg p-6 mb-8 bg-card">
          <h3 className="text-lg font-semibold mb-4">New Connection</h3>
          <div className="grid gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Database Type</label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full px-3 py-2 border rounded-lg bg-background"
              >
                <option value="postgresql">PostgreSQL</option>
                <option value="mysql">MySQL</option>
                <option value="sqlite">SQLite</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Connection String</label>
              <input
                type="text"
                value={formData.connectionString}
                onChange={(e) => setFormData({ ...formData, connectionString: e.target.value })}
                placeholder="localhost:5432/mydb"
                className="w-full px-3 py-2 border rounded-lg bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Alias (Optional)</label>
              <input
                type="text"
                value={formData.alias}
                onChange={(e) => setFormData({ ...formData, alias: e.target.value })}
                placeholder="My Database"
                className="w-full px-3 py-2 border rounded-lg bg-background"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleConnect}
                disabled={testing || !formData.connectionString}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50"
              >
                {testing ? "Testing..." : "Connect"}
              </button>
              <button
                onClick={() => setShowForm(false)}
                className="px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:opacity-90"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {connections.map((conn) => (
          <div key={conn.id} className="border rounded-lg p-4 bg-card">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <Database className="h-8 w-8 text-primary" />
                <div>
                  <h4 className="font-semibold">{conn.alias}</h4>
                  <p className="text-sm text-muted-foreground">{conn.type}</p>
                </div>
              </div>
              {conn.status === "connected" ? (
                <CheckCircle className="h-5 w-5 text-green-500" />
              ) : (
                <XCircle className="h-5 w-5 text-red-500" />
              )}
            </div>
            <button className="mt-4 text-sm text-destructive hover:underline flex items-center gap-1">
              <Trash2 className="h-4 w-4" />
              Remove
            </button>
          </div>
        ))}

        {connections.length === 0 && !showForm && (
          <div className="col-span-full text-center py-12 text-muted-foreground">
            <Database className="mx-auto h-12 w-12 mb-4 opacity-50" />
            <p>No database connections yet</p>
            <p className="text-sm">Add a connection to start querying your databases</p>
          </div>
        )}
      </div>
    </div>
  );
}