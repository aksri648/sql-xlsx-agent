# AI Data Analyst Platform - Complete Build Specification

Build a production-ready AI Data Analyst application that allows users to upload datasets, connect databases, and query data using natural language. The application should function similarly to ChatGPT for data analytics, using LangGraph for orchestration, Groq for reasoning, ChromaDB for semantic retrieval, and Tavily for external research.

---

# Primary Goal

Users should be able to:

* Upload CSV files
* Upload Excel files (.xlsx)
* Connect SQL databases
* Ask questions in plain English
* Receive answers, charts, summaries, and insights
* View generated SQL or Pandas logic
* Compare internal data against external benchmarks
* Chat conversationally with their data

No authentication.

No login system.

No signup flow.

No payments.

No user management.

Focus entirely on analytics and data intelligence.

---

# Tech Stack

Frontend

* Next.js 15
* React
* TypeScript
* TailwindCSS
* shadcn/ui
* ECharts
* React Query

Backend

* FastAPI
* Python 3.12
* LangGraph
* LangChain
* SQLAlchemy
* Pandas
* OpenPyXL

AI

* Groq API
* Configurable models
* Default: qwen/qwen3-32b

Vector Database

* ChromaDB Cloud

External Research

* Tavily Search API

Infrastructure

* Docker
* Docker Compose

---

# Required Environment Variables

GROQ_API_KEY=

CHROMA_API_KEY=

CHROMA_TENANT=

CHROMA_DATABASE=

TAVILY_API_KEY=

---

# Application Architecture

Implement a LangGraph multi-agent system.

Graph Flow:

START

→ Data Source Router

→ Schema Discovery Agent

→ Context Retrieval Agent

→ Question Understanding Agent

→ Analysis Planner Agent

→ SQL Agent OR Pandas Agent

→ Validation Agent

→ Execution Agent

→ Result Evaluator Agent

IF SUFFICIENT DATA:

→ Insight Agent

ELSE:

→ Tavily Research Agent

→ Context Merger Agent

→ Insight Agent

→ Visualization Agent

→ Response Formatter

END

Each node must be implemented as a separate LangGraph node.

---

# Agent Definitions

## Data Source Router

Determine whether the request should use:

* Uploaded files
* SQL database
* Hybrid mode

Output:

{
"source_type": "file|database|hybrid"
}

---

## Schema Discovery Agent

Responsibilities:

Extract:

* table names
* column names
* relationships
* datatypes
* row counts
* sample values

Output:

{
"schema": {}
}

---

## Context Retrieval Agent

Use ChromaDB.

Collections:

* schemas
* documentation
* glossary
* query_examples

Retrieve:

Top 10 most relevant context chunks.

Context should include:

* schema descriptions
* business definitions
* previous successful query patterns
* dataset metadata

---

## Question Understanding Agent

Extract:

* intent
* metrics
* dimensions
* filters
* grouping requirements
* date ranges

Output:

{
"intent": "",
"metrics": [],
"dimensions": [],
"filters": [],
"date_range": ""
}

---

## Analysis Planner Agent

Create an execution strategy before code generation.

Example:

Question:

"Show monthly sales by region."

Plan:

1. Use sales dataset
2. Group by month
3. Group by region
4. Aggregate revenue
5. Create line chart

Output:

{
"plan": []
}

---

## SQL Agent

Used when source_type == database

Responsibilities:

Generate optimized SQL.

Rules:

* Read-only only
* ANSI SQL
* No SELECT *
* Use aliases
* Use aggregation in SQL
* Use LIMIT when appropriate
* Use efficient joins
* Use schema context only

Forbidden:

INSERT

UPDATE

DELETE

DROP

ALTER

TRUNCATE

CREATE

MERGE

EXECUTE

Output:

{
"sql": ""
}

---

## Pandas Agent

Used when source_type == file

Generate Pandas operations.

Rules:

* Use only provided DataFrames
* No filesystem access
* No subprocess
* No shell execution
* No unsafe imports

Output:

{
"pandas_code": ""
}

Example:

df.groupby("month")["sales"].sum()

---

## Validation Agent

Validate:

SQL

Pandas code

Check:

* safety
* schema compliance
* unsupported operations
* invalid references

Reject dangerous operations.

---

## Execution Agent

Execute:

SQL using SQLAlchemy

Pandas code inside sandboxed environment

Return:

* DataFrame
* JSON result
* Statistics
* Row count

---

## Result Evaluator Agent

Determine whether sufficient information exists.

Conditions:

* empty result
* incomplete answer
* unknown business concept
* benchmark request
* market comparison request
* current event request

Output:

{
"needs_external_research": true,
"reason": ""
}

---

## Tavily Research Agent

Use Tavily when:

* external benchmark required
* market comparison required
* KPI definition required
* current information required
* dataset insufficient

Examples:

"What is average SaaS churn?"

"Compare our CAC with industry standards."

"What is EBITDA?"

"Compare our growth with market averages."

Output:

{
"research_context": [],
"sources": []
}

---

## Context Merger Agent

Combine:

1. Internal dataset insights
2. SQL/Pandas results
3. Tavily research

Priority:

Internal Data > External Research

Never overwrite actual user data with external estimates.

---

## Insight Agent

Generate:

* Executive Summary
* Key Findings
* Trends
* Anomalies
* Recommendations

Style:

Business-focused.

Concise.

Actionable.

Professional.

---

## Visualization Agent

Automatically choose chart type.

Rules:

Time Series
→ Line Chart

Comparison
→ Bar Chart

Distribution
→ Histogram

Correlation
→ Scatter Plot

Composition
→ Pie Chart

Output:

{
"chart_type": "",
"x_axis": "",
"y_axis": ""
}

---

## Response Formatter Agent

Return structured response:

{
"answer": "",
"insights": [],
"chart": {},
"generated_sql": "",
"generated_pandas": "",
"sources": [],
"follow_up_questions": []
}

---

# ChromaDB Design

Collections:

schemas

documentation

glossary

query_examples

Store metadata:

{
"table_name": "",
"column_name": "",
"description": "",
"source": "",
"embedding": ""
}

Whenever datasets or schemas are uploaded:

1. Profile dataset
2. Generate metadata
3. Generate descriptions
4. Create embeddings
5. Store in Chroma

All questions must perform retrieval before SQL or Pandas generation.

---

# File Upload System

Support:

CSV

XLSX

Requirements:

CSV:

* delimiter detection
* encoding detection

Excel:

* multi-sheet support

Each sheet becomes a virtual table.

After upload:

Generate:

* schema
* statistics
* metadata
* embeddings

Store in ChromaDB.

---

# Database Connectors

Support:

* PostgreSQL
* MySQL
* SQL Server
* SQLite

Workflow:

1. User enters connection string
2. Test connection
3. Extract schema
4. Generate metadata
5. Generate embeddings
6. Store in Chroma

Do not permanently store credentials.

Maintain active connections only during runtime.

---

# Chat Interface

Build a ChatGPT-style interface.

Features:

* streaming responses
* markdown rendering
* syntax-highlighted SQL
* syntax-highlighted Pandas code
* dataset selector
* database selector
* session history
* suggested questions
* chart rendering
* dark mode
* responsive design

---

# API Endpoints

POST /upload/csv

POST /upload/excel

POST /database/connect

POST /chat

GET /datasets

GET /schema

DELETE /dataset/{id}

GET /health

---

# LangGraph State

Create:

```python
from typing import TypedDict

class AnalystState(TypedDict):
    question: str
    source_type: str
    schema_context: dict
    retrieved_context: list
    analysis_plan: list
    generated_sql: str
    generated_pandas: str
    results: dict
    tavily_context: list
    external_sources: list
    insights: dict
    visualization: dict
    response: dict
```

Implement checkpointing and conversational memory.

---

# Security Requirements

Allow only:

SELECT queries

Prevent:

* prompt injection
* SQL injection
* arbitrary code execution
* filesystem access from generated code
* subprocess execution

Sandbox Pandas execution.

Validate all generated code before execution.

---

# Project Structure

Generate a clean monorepo structure:

/frontend

/backend

/langgraph

/agents

/services

/connectors

/vectorstore

/models

/api

/tests

/docker

/docs

---

# Frontend Pages

/

/chat

/datasets

/database

/settings

---

# Required Deliverables

Generate:

1. Complete Next.js frontend
2. Complete FastAPI backend
3. Complete LangGraph workflow
4. Groq integration
5. ChromaDB integration
6. Tavily integration
7. SQLAlchemy integration
8. Pandas execution engine
9. Dockerfile
10. Docker Compose
11. Environment configuration
12. Database schema models
13. API routes
14. Unit tests
15. Integration tests
16. README
17. Setup instructions
18. Sample datasets
19. Error handling
20. Logging system

Code must be:

* production-ready
* modular
* scalable
* typed
* documented
* maintainable
* clean architecture based

Generate the complete source code, folder structure, backend, frontend, LangGraph agents, services, API routes, Docker configuration, tests, and documentation required to run the application end-to-end.

