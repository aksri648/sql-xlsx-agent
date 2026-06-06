"use client";

import { ChartConfig } from "@/types";
import ReactECharts from "echarts-for-react";

interface ChartComponentProps {
  config: ChartConfig;
}

export function ChartComponent({ config }: ChartComponentProps) {
  const getOption = () => {
    const baseOption = {
      title: {
        text: config.title,
      },
      tooltip: {
        trigger: "axis",
      },
      xAxis: {
        type: "category",
        data: ["A", "B", "C", "D", "E"],
      },
      yAxis: {
        type: "value",
      },
      series: [
        {
          data: [12, 24, 36, 48, 60],
          type: "line",
        },
      ],
    };

    switch (config.chart_type) {
      case "line":
        return baseOption;
      case "bar":
        return {
          ...baseOption,
          series: [{ ...baseOption.series[0], type: "bar" }],
        };
      case "pie":
        return {
          ...baseOption,
          xAxis: { show: false },
          series: [
            {
              data: [
                { value: 12, name: "A" },
                { value: 24, name: "B" },
                { value: 36, name: "C" },
              ],
              type: "pie",
            },
          ],
        };
      case "scatter":
        return {
          ...baseOption,
          series: [{ ...baseOption.series[0], type: "scatter" }],
        };
      default:
        return baseOption;
    }
  };

  return (
    <div className="border rounded-lg p-4 bg-background">
      <ReactECharts option={getOption()} style={{ height: 300 }} />
    </div>
  );
}