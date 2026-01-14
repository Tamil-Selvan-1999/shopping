# Quickstart - Shopping POC

Prerequisites:

- Python 3.11+
- Node.js + npm
- MongoDB running locally or reachable via `MONGO_URL`

Start backend:

```powershell
cd src/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Start frontend:

```bash
cd src/frontend
npm install
npm run dev
```

Open the frontend at `http://localhost:3000` and the API at `http://localhost:8000`.
