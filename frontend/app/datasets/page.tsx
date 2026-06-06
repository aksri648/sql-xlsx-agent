"use client";

import { useState } from "react";
import { Upload, FileSpreadsheet, X, CheckCircle } from "lucide-react";

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
    <div className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Datasets</h1>

      <div
        className={`border-2 border-dashed rounded-lg p-12 text-center mb-8 transition-colors ${
          dragActive ? "border-primary bg-primary/5" : "border-border"
        }`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
        <h3 className="text-lg font-semibold mb-2">Upload Files</h3>
        <p className="text-muted-foreground mb-4">
          Drag and drop CSV or Excel files here, or click to browse
        </p>
        <label className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg cursor-pointer hover:opacity-90">
          <FileSpreadsheet className="h-4 w-4" />
          Browse Files
          <input
            type="file"
            className="hidden"
            accept=".csv,.xlsx,.xls"
            multiple
            onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
          />
        </label>
      </div>

      {uploading && (
        <div className="flex items-center gap-2 mb-4">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
          <span>Uploading...</span>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {datasets.map((dataset) => (
          <div
            key={dataset.id}
            className="border rounded-lg p-4 bg-card"
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <h4 className="font-semibold">{dataset.name}</h4>
                <p className="text-sm text-muted-foreground">
                  {dataset.source_type} • {dataset.row_count} rows
                </p>
              </div>
              <CheckCircle className="h-5 w-5 text-green-500" />
            </div>
            <div className="flex flex-wrap gap-2">
              {dataset.columns?.slice(0, 3).map((col: any, i: number) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded"
                >
                  {col.name}
                </span>
              ))}
              {(dataset.columns?.length || 0) > 3 && (
                <span className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded">
                  +{(dataset.columns?.length || 0) - 3} more
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}