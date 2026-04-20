# october_21st_birthday
I'm creating a full stack interactive experience for my girlfriend's 21st birthday. I'm also using it to experiment with cursor and using multiple agents to code a full stack web app. I'll try to experiment with angular. 

## Current stack
- Frontend: Angular + TypeScript (`apps/web`)
- Backend: FastAPI + Python (`apps/api`)
- Database: MongoDB (schema in `docs/database_design_v1.md`)

## Quick start

### API
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### Web
```bash
cd apps/web
npm install
npm start
```
