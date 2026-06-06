# AI Data Analyst Platform

A production-ready AI Data Analyst application that allows users to upload datasets, connect databases, and query data using natural language.

## Features

- **File Upload**: Upload CSV and Excel files for analysis
- **Database Connection**: Connect to PostgreSQL, MySQL, or SQLite databases
- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered Analysis**: Uses LangGraph for orchestration with Groq AI
- **Semantic Search**: ChromaDB for context retrieval
- **External Research**: Tavily API for market benchmarks
- **Interactive Charts**: ECharts visualization
- **Streaming Responses**: Real-time AI responses

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   FastAPI   │────▶│  LangGraph  │
│  (Next.js)  │     │   Backend   │     │  Workflow   │
└─────────────┘     └─────────────┘     └─────────────┘
                         │                    │
                         ▼                    ▼
                   ┌─────────────┐     ┌─────────────┐
                   │   ChromaDB  │     │    Groq     │
                   │  (Vectors)  │     │    AI       │
                   └─────────────┘     └─────────────┘
```

## Tech Stack

### Frontend
- Next.js 15
- React 18
- TypeScript
- TailwindCSS
- ECharts
- React Query

### Backend
- FastAPI
- Python 3.12
- LangGraph
- LangChain
- SQLAlchemy
- Pandas

### AI & Data
- Groq API (qwen/qwen3-32b)
- ChromaDB Cloud
- Tavily Search API

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (for containerized deployment)

### Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sql_tavily
```

2. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

3. Fill in your API keys in `.env`:
```
GROQ_API_KEY=your_groq_api_key
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_tenant
CHROMA_DATABASE=your_database
TAVILY_API_KEY=your_tavily_api_key
```

### Docker Deployment (Recommended)

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Development Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/upload/csv` | Upload CSV file |
| POST | `/upload/excel` | Upload Excel file |
| POST | `/database/connect` | Connect to database |
| POST | `/chat` | Send chat message |
| POST | `/chat/stream` | Stream chat response |
| GET | `/datasets` | List datasets |
| GET | `/datasets/{id}` | Get dataset details |
| DELETE | `/datasets/{id}` | Delete dataset |

## Project Structure

```
sql_tavily/
├── backend/
│   ├── api/              # API routes
│   ├── agents/           # LangGraph agents
│   ├── connectors/       # Database connectors
│   ├── langgraph/        # LangGraph workflow
│   │   └── nodes/        # Individual agent nodes
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   └── vectorstore/      # ChromaDB integration
├── frontend/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   ├── lib/              # Utilities
│   └── types/            # TypeScript types
├── docker/               # Docker configurations
├── tests/                # Test suite
├── docker-compose.yml    # Docker Compose configuration
└── context.md           # Build progress tracking
```

## LangGraph Workflow

The application uses a multi-agent LangGraph system:

1. **Data Source Router** - Determines data source type
2. **Schema Discovery Agent** - Extracts schema information
3. **Context Retrieval Agent** - Retrieves relevant context from ChromaDB
4. **Question Understanding Agent** - Parses user intent
5. **Analysis Planner Agent** - Creates execution strategy
6. **SQL Agent / Pandas Agent** - Generates appropriate code
7. **Validation Agent** - Validates generated code
8. **Execution Agent** - Runs the code
9. **Result Evaluator Agent** - Evaluates results
10. **Tavily Research Agent** - (Optional) External research
11. **Insight Agent** - Generates insights
12. **Visualization Agent** - Chooses chart type
13. **Response Formatter Agent** - Formats final response

## Testing

```bash
cd backend
pytest tests/ -v
```

## Security

- Read-only SQL queries enforced
- No filesystem access from generated code
- Sandboxed Pandas execution
- Input validation on all endpoints
- No credentials stored permanently

## License

MIT