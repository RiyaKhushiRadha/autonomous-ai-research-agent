# 🤖 Autonomous AI Research Agent

An agentic AI research system that plans, searches the web, retrieves from uploaded documents, synthesizes an answer, and **verifies its own output** before returning it — built with LangGraph, LangChain, RAG, and FastAPI.

---

## 🚀 Live Demo

* **API Base URL:** https://autonomous-ai-research-agent-awf7.onrender.com
* **Swagger UI:** https://autonomous-ai-research-agent-awf7.onrender.com/docs
* **ReDoc:** https://autonomous-ai-research-agent-awf7.onrender.com/redoc

> ⚠️ Hosted on Render's free tier — the first request after inactivity may take 30–60s or more to wake up (cold start). The base URL itself returns `{"detail": "Not Found"}` since there's no root route — use `/docs` to explore the API.

---

## ✨ Features

- **Multi-agent research workflow** orchestrated with LangGraph (planner → web research → document research → synthesis → verification)
- **Self-verification loop** — the agent checks its own answer against the evidence and retries (up to a configurable limit) if unsupported
- **RAG over uploaded documents** — upload PDF, DOCX, or TXT files; the agent retrieves relevant chunks using local sentence-transformer embeddings
- **Live web research** via Tavily search
- **Graceful degradation** — if web search or document retrieval fails (or no documents are uploaded), the agent falls back to general knowledge and says so explicitly, instead of refusing to answer
- **Full REST API** with document management and research history endpoints

---

## 🏗️ Architecture

```
                    ┌─────────────┐
                    │   Planner   │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ Web Research│  (Tavily)
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ RAG Research│  (uploaded docs)
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │  Synthesis  │  (Gemini)
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
              ┌─────│ Verification│
              │     └──────┬──────┘
              │            │ verified
       not verified        ▼
       (retry, up to      END
        MAX_RETRIES)
              │
              └──────► back to Synthesis
```

The state machine is built with **LangGraph**, where each node updates a shared `ResearchState` (query, plan, web/RAG results, final answer, verification result, retry count).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Agent Orchestration | LangGraph |
| LLM | Google Gemini (`gemini-2.5-flash`) via `langchain-google-genai` |
| Web Search | Tavily (`langchain-tavily`) |
| Embeddings | Google Gemini (`text-embedding-004`) via `langchain-google-genai` |
| Document Parsing | `pypdf`, `python-docx` |
| Text Splitting | `langchain-text-splitters` |
| Testing | `pytest`, `pytest-asyncio`, `httpx` |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/documents/upload` | Upload a PDF/DOCX/TXT document for RAG (max 10 MB) |
| `GET` | `/documents` | List all indexed documents |
| `DELETE` | `/documents/{document_id}` | Delete a document and its vectors |
| `POST` | `/research` | Submit a research query, run the full agent workflow |
| `GET` | `/research/{research_id}` | Retrieve a past research result by ID |

Full interactive docs available at `/docs` (Swagger) once running.

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/RiyaKhushiRadha/autonomous-ai-research-agent.git
cd autonomous-ai-research-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```
```env
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Run the server
```bash
fastapi dev app/main.py
```
The API will be live at `http://localhost:8000`, docs at `http://localhost:8000/docs`.

---

## 🧪 Running Tests

```bash
pytest
```

All 22 tests cover: health check, document upload/list/delete (incl. validation for unsupported types, empty files, oversized files), RAG retrieval, the full LangGraph research workflow, verification retry logic, and graceful failure handling for LLM/web-search/retrieval errors.

---

## 📁 Project Structure

```
app/
├── agents/          # LangGraph state, nodes, graph, prompts
├── api/routes/      # FastAPI route handlers (health, documents, research)
├── config/          # Settings (pydantic-settings)
├── models/          # Pydantic request/response schemas
├── rag/             # Document loading, splitting, embeddings, vector store, retriever
├── services/        # Business logic (document_service, llm_service, research_service)
├── tools/           # LangChain tools (web_search, retrieval)
└── main.py          # FastAPI app entrypoint
tests/               # pytest suite
```

---

## 🔮 Future Improvements

- Persistent vector store (currently in-memory; resets on server restart)
- Slack integration for querying the agent directly from Slack
- Streaming responses for long-running research queries
- Support for more document types (CSV, HTML)

---

# 📜 License

This project is licensed under the MIT License.

See the LICENSE file for more information.

---

# 👩‍💻 Author

**Riya**

- GitHub: https://github.com/RiyaKhushiRadha
- LinkedIn: https://www.linkedin.com/in/riya-5a137932a/

If you found this project useful, consider giving it a ⭐ on GitHub.
