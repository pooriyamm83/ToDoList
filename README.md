## Phase 3 - Web API (FastAPI)
- CLI deprecated and fully replaced with RESTful API
- Layered Architecture: controllers → services → repositories → models
- Pydantic schemas for request/response validation
- Auto-generated documentation: http://localhost:8000/docs
- All 9 features from Phase 1 implemented as endpoints

### Run
```bash
poetry run uvicorn app.main:app --reload
