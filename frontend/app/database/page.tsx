"use client";

import { useState } from "react";
import { Database, Plus, Trash2, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";

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
    <div className="container py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Database Connections</h1>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Add Connection
        </Button>
      </div>

      {showForm && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>New Connection</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="db-type">Database Type</Label>
              <select
                id="db-type"
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="postgresql">PostgreSQL</option>
                <option value="mysql">MySQL</option>
                <option value="sqlite">SQLite</option>
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="conn-string">Connection String</Label>
              <Input
                id="conn-string"
                value={formData.connectionString}
                onChange={(e) => setFormData({ ...formData, connectionString: e.target.value })}
                placeholder="localhost:5432/mydb"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="alias">Alias (Optional)</Label>
              <Input
                id="alias"
                value={formData.alias}
                onChange={(e) => setFormData({ ...formData, alias: e.target.value })}
                placeholder="My Database"
              />
            </div>
            <div className="flex gap-2">
              <Button
                onClick={handleConnect}
                disabled={testing || !formData.connectionString}
              >
                {testing ? "Testing..." : "Connect"}
              </Button>
              <Button variant="outline" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {connections.map((conn) => (
          <Card key={conn.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Database className="h-8 w-8 text-primary" />
                  <div>
                    <CardTitle className="text-base">{conn.alias}</CardTitle>
                    <Badge variant="secondary" className="mt-1">
                      {conn.type}
                    </Badge>
                  </div>
                </div>
                {conn.status === "connected" && (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                )}
              </div>
            </CardHeader>
            <CardContent>
              <Button variant="ghost" size="sm" className="text-destructive">
                <Trash2 className="mr-2 h-4 w-4" />
                Remove
              </Button>
            </CardContent>
          </Card>
        ))}

        {connections.length === 0 && !showForm && (
          <Card className="col-span-full border-dashed">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Database className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="font-medium">No database connections yet</p>
              <p className="text-sm text-muted-foreground">
                Add a connection to start querying your databases
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}