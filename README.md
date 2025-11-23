# NetResearch Backend

**NetResearch** is an intelligent research collaboration platform that helps students and researchers discover relevant professors and research opportunities through AI-powered analysis and interactive 3D graph visualization.

## Architecture Overview

This project is split into two separate repositories:
- **Backend** (this repository): FastAPI-based REST API handling agent orchestration, LLM interactions, and data processing
- **Frontend** (separate repository): React-based web interface with 3D graph visualization

## Key Features

- **AI-Powered Query Analysis**: Extracts research topics, geographical preferences, and institutions from natural language queries
- **Academic Paper Discovery**: Searches OpenAlex API for relevant research papers based on user interests
- **Professor Extraction**: Identifies and profiles researchers from academic papers with institutional affiliations
- **CV Analysis**: Processes uploaded CVs to extract research expertise and match with relevant professors
- **Email Generation**: Creates personalized collaboration emails using LLM
- **3D Graph Visualization**: Builds relationship networks between researchers and institutions
- **Persistent Storage**: SQLite database for saving research runs and user data

## Tech Stack

### Core Framework
- **FastAPI**: Modern async web framework for building APIs
- **Python 3.11+**: Primary programming language
- **Pydantic**: Data validation and settings management

### AI & Agent Orchestration
- **pyagentspec**: Agent specification framework for LLM interactions
- **wayflowcore**: Agent execution and workflow management
- **Together AI**: LLM provider (OpenAI-compatible API)

### External APIs
- **OpenAlex API**: Academic research paper and author database
- **Semantic Scholar API**: Fallback for paper abstracts

### Data Processing
- **PyPDF2**: PDF parsing for CV extraction
- **Requests**: HTTP client for external API calls

### Database
- **SQLite**: Lightweight embedded database for data persistence

## Project Structure

```
netresearch-backend/
├── app/
│   ├── agents/                  # AI agent implementations
│   │   ├── orchestrator.py      # Main pipeline coordinator
│   │   ├── intent_agent.py      # Query analysis agent
│   │   ├── search_agent.py      # Paper search agent
│   │   ├── extraction_agent.py  # Professor extraction agent
│   │   └── models.py            # Agent data models
│   │
│   ├── routers/                 # FastAPI route handlers
│   │   ├── agent.py             # Agent run endpoints
│   │   ├── cv.py                # CV upload endpoint
│   │   ├── email.py             # Email generation endpoint
│   │   └── user.py              # User management endpoint
│   │
│   ├── schemas/                 # Pydantic models for API
│   │   └── agent.py             # Request/response schemas
│   │
│   ├── services/                # Business logic services
│   │   ├── state_manager.py    # In-memory state management
│   │   ├── cv_service.py        # CV processing service
│   │   └── email_service.py     # Email generation service
│   │
│   ├── utils/                   # Utility functions
│   │   ├── openalex_client.py  # OpenAlex API client
│   │   ├── abstract_fetcher.py # Paper abstract retrieval
│   │   ├── paper_mapper.py      # Paper data mapping
│   │   ├── professor_mapper.py  # Professor data mapping
│   │   └── graph_builder.py     # Graph construction logic
│   │
│   ├── prompts/                 # LLM system prompts
│   │   └── intent_extraction.py
│   │
│   ├── database/                # Database layer
│   │   └── database.py          # SQLite database operations
│   │
│   ├── core/                    # Core configuration
│   │   ├── config.py            # Settings and environment config
│   │   └── llm_factory.py       # LLM client factory
│   │
│   └── main.py                  # FastAPI application entry point
│
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Together AI API key (for LLM access)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd netresearch-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your Together AI API key:
```env
TOGETHER_API_KEY=your_together_ai_api_key_here
MODEL_NAME=moonshotai/Kimi-K2-Instruct-0905
TOGETHER_BASE_URL=https://api.together.xyz/v1
```

### 5. Run the Application
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Usage

### API Documentation
Once the server is running, access the interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main API Endpoints

#### 1. Start Agent Run
```bash
POST /agent/run
Content-Type: application/json

{
  "query": "I'm looking for professors working on machine learning at ETH Zurich",
  "cv_id": "optional-cv-id",
  "max_nodes": 10
}
```

Returns:
```json
{
  "run_id": "uuid",
  "status": "running"
}
```

#### 2. Poll Agent Status
```bash
GET /agent/status/{run_id}
```

Returns real-time progress with:
- Step-by-step pipeline updates (filters, search, extraction, relationships, graph)
- Extracted topics, geographical areas, and institutions
- Found papers (preview)
- Extracted professors
- Final graph data with nodes and links

#### 3. Upload CV
```bash
POST /cv/upload
Content-Type: multipart/form-data

file: <pdf-file>
```

#### 4. Generate Email
```bash
POST /email/generate
Content-Type: application/json

{
  "professor_id": "professor-node-id",
  "email_type": "colab" | "reach_out",
  "cv_id": "optional-cv-id"
}
```

#### 5. Set User Name
```bash
POST /user/set-name
Content-Type: application/json

{
  "name": "Your Name"
}
```

## Pipeline Overview

The agent orchestrator executes a 5-step pipeline:

1. **Intent & Filter Extraction**: Analyzes user query to extract topics, geographical areas, and institutions
2. **Paper Search**: Queries OpenAlex API for relevant research papers (last 2 years)
3. **Professor Extraction**: Identifies authors from papers and fetches their profiles
4. **Relationship Building**: Creates hierarchical links between professors based on institutions
5. **Graph Construction**: Builds final 3D graph with user node connected to research network

## Database Schema

SQLite database (`netresearch.db`) with two tables:

- **users**: Stores user information (name)
- **runs**: Stores research run history with query and graph data (JSON)

## Development Notes

### State Management
The application uses an in-memory `StateManager` for real-time run progress tracking during active sessions. Completed runs are persisted to SQLite.

### LLM Configuration
All LLM calls use pyagentspec with Together AI as the provider. The configuration supports OpenAI-compatible APIs through the `OpenAiCompatibleConfig`.

### External API Rate Limits
- OpenAlex: No authentication required, polite pool recommended
- Semantic Scholar: Fallback for missing abstracts, includes small delays

## CORS Configuration

CORS is configured to allow requests from `http://localhost:3000` (React frontend). Modify `app/core/config.py` to change allowed origins.

## Contributing

This project was developed during a hackathon. For contributions or issues, please contact the repository maintainers.

## Acknowledgments

- **OpenAlex** for providing open access to academic research data
- **Together AI** for LLM infrastructure