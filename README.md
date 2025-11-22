# DeepScience Agent Backend

FastAPI backend for the DeepScience Agent - 3D Research Graph Visualization

## Project Structure

```
netresearch-backend/
├── app/
│   ├── main.py              # FastAPI app with CORS
│   ├── routers/             # API endpoints
│   │   ├── cv.py            # CV upload endpoint
│   │   └── agent.py         # Agent run & status endpoints
│   ├── schemas/             # Pydantic models
│   │   ├── cv.py            # CV schemas
│   │   └── agent.py         # Agent schemas
│   └── services/            # Business logic
│       ├── state_manager.py # In-memory state storage
│       └── simulation_service.py # Mock agent simulation
├── requirements.txt
└── README.md
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. CV Upload
**POST** `/api/cv/upload`
- Upload a PDF CV file
- Returns: `cv_id`, `message`, `extracted_concepts`

```bash
curl -X POST "http://localhost:8000/api/cv/upload" \
  -F "file=@path/to/cv.pdf"
```

### 2. Start Agent Run
**POST** `/api/agent/run`
- Start a new research graph generation
- Body: `{ "query": "Diffusion Models", "cv_id": "optional", "max_nodes": 10 }`
- Returns: `run_id`, `status`

```bash
curl -X POST "http://localhost:8000/api/agent/run" \
  -H "Content-Type: application/json" \
  -d '{"query": "Diffusion Models", "max_nodes": 10}'
```

### 3. Poll Status
**GET** `/api/agent/status/{run_id}`
- Check the status of a running agent
- Returns: `run_id`, `status`, `steps`, `graph_data`

```bash
curl "http://localhost:8000/api/agent/status/{run_id}"
```

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## CORS

CORS is configured to allow requests from `http://localhost:3000` (React frontend)

## State Management

This is a hackathon project using **in-memory storage**. All data is lost on server restart.
- CV data stored in `state_manager.cv_store`
- Run data stored in `state_manager.run_store`