# AI Newsroom Platform — Phase 1

A production-ready AI-powered newsroom platform built with **Python**, **FastAPI**, **Docker**, and a **provider-agnostic LLM architecture**. The platform automates news research, article writing, and fact-checking through three independent microservices.

---

## Architecture

```
+--------------------------------------------------------------+
|                     docker-compose.yml                        |
|                                                               |
|  +--------------+  +--------------+  +-------------------+   |
|  |  Research     |  |  AI Writer   |  |  Fact-Check       |   |
|  |  Service      |  |  Service     |  |  Service          |   |
|  |  :8004        |  |  :8002       |  |  :8003            |   |
|  |               |  |              |  |                   |   |
|  |  POST /research|  | POST /generate|  | POST /verify    |   |
|  |  GET  /health |  |  GET  /health|  |  GET  /health     |   |
|  +------+--------+  +------+-------+  +--------+----------+  |
|         |                  |                    |              |
|         +------------------+--------------------+             |
|                            |                                  |
|               +------------v------------+                     |
|               |    shared/utils/        |                     |
|               |   LLM Provider Manager  |                     |
|               |                         |                     |
|               |  +-------+ +-------+    |                     |
|               |  | Ollama| | Groq  |    |                     |
|               |  | (HTTP)| | (SDK) |    |                     |
|               |  +-------+ +-------+    |                     |
|               |  +-------+ +--------+   |                     |
|               |  |Gemini | | NVIDIA |   |                     |
|               |  | (SDK) | | (HTTP) |   |                     |
|               |  +-------+ +--------+   |                     |
|               +-------------------------+                     |
+---------------------------------------------------------------+
```

### Clean Architecture Layers (per service)

```
Routes (API endpoints)
  --> Services (Business logic)
       --> Repository (Data access -- placeholder for PostgreSQL)
            --> LLM Provider (via shared/utils/)
```

---

## Quick Start

### Prerequisites

- **Python 3.9+** with `pip` (for local development)
- **Docker** and **Docker Compose** (for production deployment)
- An LLM provider configured (Ollama local, or API key for Groq/Gemini/NVIDIA)

### 1. Setup

```bash
# Clone the repo
git clone <repo-url> && cd AI_News

# Create your .env file
cp .env.example .env

# Configure your LLM provider in .env
# Edit LLM_PROVIDER and the corresponding API key/URL
```

### 2. Local Development (Python)

Run all three services with a single command:

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Start all services
python main.py
```

This starts all three microservices as parallel subprocesses:

| Service | URL | Swagger Docs |
|---------|-----|--------------|
| Research Service | http://localhost:8004 | http://localhost:8004/docs |
| AI Writer Service | http://localhost:8002 | http://localhost:8002/docs |
| Fact-Check Service | http://localhost:8003 | http://localhost:8003/docs |

Press `Ctrl+C` to stop all services. If any service crashes, all others are automatically stopped.

### 3. Production Deployment (Docker)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up --build -d

# Stop all services
docker-compose down
```

> **Note:** When running via Docker, set `OLLAMA_BASE_URL=http://host.docker.internal:11434` in your `.env`
> so containers can reach Ollama running on the host machine.

---

## LLM Provider Configuration

Set `LLM_PROVIDER` in your `.env` file to switch providers. **No code changes needed** — the provider manager automatically routes requests to the configured provider.

| Provider | `LLM_PROVIDER` | Required Keys | Communication |
|----------|----------------|---------------|---------------|
| Ollama   | `ollama`       | `OLLAMA_BASE_URL`, `OLLAMA_MODEL` | HTTP via httpx (`/api/chat`) |
| Groq     | `groq`         | `GROQ_API_KEY`, `GROQ_MODEL` | SDK (`groq`) |
| Gemini   | `gemini`       | `GEMINI_API_KEY`, `GEMINI_MODEL` | SDK (`google-genai`) |
| NVIDIA NIM | `nvidia`     | `NVIDIA_API_KEY`, `NVIDIA_BASE_URL`, `NVIDIA_MODEL` | HTTP via httpx |

### Example: Using Groq

```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Example: Using Gemini

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

### Example: Using Local Ollama

```env
LLM_PROVIDER=ollama
# Use localhost for local dev (python main.py)
OLLAMA_BASE_URL=http://localhost:11434
# Use host.docker.internal for Docker deployment
# OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3
```

### Example: Using NVIDIA NIM

```env
LLM_PROVIDER=nvidia
NVIDIA_API_KEY=your_nvidia_api_key_here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=meta/llama-3.1-8b-instruct
```

---

## API Reference

### Research Service — `POST /research`

**Request:**
```json
{
  "topic": "AI in Education"
}
```

**Response:**
```json
{
  "topic": "AI in Education",
  "research": "Comprehensive research notes...",
  "references": [
    "Source Name - Title (Year): Description",
    "..."
  ]
}
```

### AI Writer Service — `POST /generate`

**Request:**
```json
{
  "topic": "AI in Education",
  "research": "Research notes from the research service..."
}
```

**Response:**
```json
{
  "headline": "How AI Is Transforming Modern Education",
  "summary": "A concise summary of the article...",
  "article": "Full article body...",
  "seo_title": "AI in Education: Trends and Impact | 2025",
  "meta_description": "Discover how AI is reshaping education..."
}
```

### Fact-Check Service — `POST /verify`

**Request:**
```json
{
  "article": "Full article text to verify...",
  "topic": "AI in Education"
}
```

**Response:**
```json
{
  "status": "verified",
  "confidence_score": 95,
  "issues": [],
  "recommendations": ["Consider adding more recent statistics"]
}
```

### Health Check — `GET /health` (all services)

```json
{
  "status": "healthy",
  "service": "research_service",
  "version": "0.1.0",
  "timestamp": "2025-01-01T00:00:00Z",
  "llm_provider": "ollama"
}
```

---

## Project Structure

```
AI_News/
├── main.py                     # Local dev entry point (runs all 3 services)
├── docker-compose.yml          # Production orchestration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .env                        # Your local config (git-ignored)
├── validate_syntax.py          # Syntax validation for all .py files
├── README.md
│
├── shared/                     # Shared library (used by all services)
│   ├── __init__.py
│   ├── setup.py
│   ├── config.py               # Centralized Settings (pydantic-settings)
│   ├── logging.py              # Structured logging setup
│   ├── exceptions.py           # Custom exception hierarchy
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── llm_base.py         # BaseLLMProvider (abstract class)
│   │   ├── llm_factory.py      # get_llm_provider() factory
│   │   ├── llm_ollama.py       # OllamaProvider (httpx, /api/chat)
│   │   ├── llm_groq.py         # GroqProvider (groq SDK)
│   │   ├── llm_gemini.py       # GeminiProvider (google-genai SDK)
│   │   └── llm_nvidia.py       # NvidiaProvider (httpx)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── research.py         # Research request/response models
│   │   ├── writer.py           # Writer request/response models
│   │   ├── fact_check.py       # Fact-check request/response models
│   │   └── health.py           # Health check response model
│   └── prompts/
│       ├── __init__.py
│       ├── research_prompts.py
│       ├── writer_prompts.py
│       └── fact_check_prompts.py
│
├── research_service/           # Port 8004 (local) / 8001 (Docker)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py             # FastAPI application
│       ├── config.py           # Service-specific config
│       ├── dependencies.py     # Dependency injection
│       ├── routes/
│       │   ├── __init__.py
│       │   └── research.py     # POST /research, GET /health
│       ├── services/
│       │   ├── __init__.py
│       │   └── service.py      # ResearchService (business logic)
│       ├── repositories/
│       │   ├── __init__.py
│       │   └── repository.py   # ResearchRepository (DB placeholder)
│       └── agents/
│           ├── __init__.py
│           └── research_agent.py
│
├── ai_writer_service/          # Port 8002
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── dependencies.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── writer.py       # POST /generate, GET /health
│       ├── services/
│       │   ├── __init__.py
│       │   └── service.py      # WriterService (5-step LLM pipeline)
│       ├── repositories/
│       │   ├── __init__.py
│       │   └── repository.py   # ArticleRepository (DB placeholder)
│       └── agents/
│           └── __init__.py
│
└── fact_check_service/         # Port 8003
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── __init__.py
        ├── main.py
        ├── config.py
        ├── dependencies.py
        ├── routes/
        │   ├── __init__.py
        │   └── verify.py       # POST /verify, GET /health
        ├── services/
        │   ├── __init__.py
        │   └── service.py      # FactCheckService (business logic)
        ├── repositories/
        │   ├── __init__.py
        │   └── repository.py   # FactCheckRepository (DB placeholder)
        └── agents/
            ├── __init__.py
            └── fact_checker.py
```

---

## Testing the Services

### Health Checks

```bash
# Local development
curl http://localhost:8004/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### Full Pipeline Test

```bash
# Step 1: Research a topic
curl -X POST http://localhost:8004/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI in Education"}'

# Step 2: Generate article (paste research output)
curl -X POST http://localhost:8002/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI in Education", "research": "<paste research output here>"}'

# Step 3: Fact-check the article (paste article output)
curl -X POST http://localhost:8003/verify \
  -H "Content-Type: application/json" \
  -d '{"article": "<paste article output here>", "topic": "AI in Education"}'
```

### PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Uri http://localhost:8004/health

# Research
Invoke-RestMethod -Uri http://localhost:8004/research -Method POST `
  -ContentType "application/json" `
  -Body '{"topic": "AI in Education"}'
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Runtime environment |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `DEBUG` | `false` | Enable debug mode |
| `LLM_PROVIDER` | `groq` | Active LLM provider (`ollama`, `groq`, `gemini`, `nvidia`) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3` | Ollama model name |
| `GROQ_API_KEY` | — | Groq API key |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model name |
| `GEMINI_API_KEY` | — | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model name |
| `NVIDIA_API_KEY` | — | NVIDIA NIM API key |
| `NVIDIA_BASE_URL` | `https://integrate.api.nvidia.com/v1` | NVIDIA NIM endpoint |
| `NVIDIA_MODEL` | `meta/llama-3.1-8b-instruct` | NVIDIA model name |

---

## Troubleshooting

### Ollama 404 Error on `/api/generate`

If you see `404 Not Found for url .../api/generate`, your Ollama version uses the newer `/api/chat` endpoint. The code has been updated to use `/api/chat`. Make sure you **restart the services** after any code changes:

```bash
# Press Ctrl+C to stop, then re-run
python main.py
```

### Port Already in Use

If a port is occupied (e.g., `[WinError 10013]`), edit the port in `main.py` under the `SERVICES` config, or find and kill the blocking process:

```bash
netstat -ano | findstr ":8004"
taskkill /PID <pid> /F
```

### Docker: Ollama Connection Refused

When running via Docker, containers cannot reach `localhost` on the host. Set:
```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

## Future Roadmap (Phase 2+)

- **PostgreSQL** — Persistent storage for articles, research, and fact-check results
- **Redis** — Caching layer and task queue
- **Qdrant** — Vector database for semantic search and embeddings
- **Gateway Service** — API gateway with authentication and rate limiting
- **Pipeline Orchestrator** — Chains research -> writer -> fact-check automatically
- **News Collection Service** — RSS/API crawlers for source material
- **Editor Service** — Grammar, readability, and style improvements
- **Newsletter Service** — PDF generation and email distribution

---

## License

This project is for internal use. See LICENSE file for details.