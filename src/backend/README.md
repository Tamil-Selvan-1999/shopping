# Shopping POC - Backend

Run the FastAPI backend (from `src/backend`):

```powershell
# create venv, install requirements
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# run (defaults: MONGO_URL=mongodb://localhost:27017)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Environment variables:

- `MONGO_URL` – MongoDB connection string (default: `mongodb://localhost:27017`)
- `MONGO_DB` – database name (default: `shopping_poc`)
- `JWT_SECRET` – secret used to sign JWT tokens (default: `change-me-for-prod`)
- `ADMIN_EMAIL` – email of the admin account allowed to create products (optional for POC)

Seed admin user:

```powershell
# Set ADMIN_EMAIL and ADMIN_PASSWORD, then run:
$env:ADMIN_EMAIL = 'admin@example.com'
$env:ADMIN_PASSWORD = 'admin123'
python .\scripts\seed_admin.py
```

The script prints a JWT token you can use for admin requests (or you can log in via `/api/v1/auth/login`).
