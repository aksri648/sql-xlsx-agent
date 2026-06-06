"use client";

import { useState } from "react";
import { Upload, FileSpreadsheet, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function DatasetsPage() {
  const [uploading, setUploading] = useState(false);
  const [datasets, setDatasets] = useState<any[]>([]);
  const [dragActive, setDragActive] = useState(false);

  const handleFileUpload = async (files: FileList) => {
    setUploading(true);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    for (const file of Array.from(files)) {
      const formData = new FormData();
      formData.append("file", file);

      const endpoint = file.name.endsWith(".csv") ? "/upload/csv" : "/upload/excel";

      try {
        const response = await fetch(`${apiUrl}${endpoint}`, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setDatasets((prev) => [...prev, data]);
        }
      } catch (error) {
        console.error("Upload failed:", error);
      }
    }

    setUploading(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files) {
      handleFileUpload(e.dataTransfer.files);
    }
  };

  return (
    <div className="container py-8">
      <h1 className="text-3xl font-bold mb-8">Datasets</h1>

      <Card
        className={`mb-8 border-dashed border-2 transition-colors ${
          dragActive ? "border-primary bg-primary/5" : ""
        }`}
      >
        <CardContent
          className="flex flex-col items-center justify-center py-12"
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
        >
          <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">Upload Files</h3>
          <p className="text-muted-foreground mb-4 text-center">
            Drag and drop CSV or Excel files here, or click to browse
          </p>
          <Button asChild>
            <label className="cursor-pointer">
              <FileSpreadsheet className="mr-2 h-4 w-4" />
              Browse Files
              <input
                type="file"
                className="hidden"
                accept=".csv,.xlsx,.xls"
                multiple
                onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
              />
            </label>
          </Button>
        </CardContent>
      </Card>

      {uploading && (
        <div className="flex items-center gap-2 mb-4">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
          <span>Uploading...</span>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {datasets.map((dataset) => (
          <Card key={dataset.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-base">{dataset.name}</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    {dataset.source_type} • {dataset.row_count} rows
                  </p>
                </div>
                <CheckCircle className="h-5 w-5 text-green-500" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {dataset.columns?.slice(0, 3).map((col: any, i: number) => (
                  <Badge key={i} variant="secondary">
                    {col.name}
                  </Badge>
                ))}
                {(dataset.columns?.length || 0) > 3 && (
                  <Badge variant="outline">
                    +{(dataset.columns?.length || 0) - 3} more
                  </Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}