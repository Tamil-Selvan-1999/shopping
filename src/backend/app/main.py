from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from bson.objectid import ObjectId
from . import db, auth, schemas
import asyncio

app = FastAPI(title="Shopping POC API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_user_from_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    token = parts[1]
    try:
        payload = auth.decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload.get("sub")


def get_optional_user_from_token(authorization: Optional[str] = Header(None)):
    """Return user id from bearer token or None when no Authorization header provided.

    If the header is present but invalid, raise 401. If header missing, return None (guest).
    """
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    token = parts[1]
    try:
        payload = auth.decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload.get("sub")


@app.on_event("startup")
async def startup_db_client():
    # ensure lazy client exists
    db.get_client()


@app.get("/api/v1/products")
async def list_products():
    database = db.get_db()
    docs = []
    async for p in database["products"].find():
        p["id"] = str(p["_id"])
        p.pop("_id", None)
        docs.append(p)
    return docs


@app.post("/api/v1/products")
async def create_product(
    product: schemas.ProductIn, user: str = Depends(get_user_from_token)
):
    # Only admin may create products for the POC. Admin identified by ADMIN_EMAIL env var.
    database = db.get_db()
    try:
        user_doc = await database["users"].find_one({"_id": ObjectId(user)})
    except Exception:
        user_doc = None
    import os

    admin_email = os.environ.get("ADMIN_EMAIL")
    if not user_doc or (admin_email and user_doc.get("email") != admin_email):
        raise HTTPException(status_code=403, detail="Requires admin privileges")
    res = await database["products"].insert_one(product.dict())
    return {"id": str(res.inserted_id)}


@app.post("/api/v1/auth/register", response_model=schemas.Token)
async def register(user: schemas.UserCreate):
    database = db.get_db()
    existing = await database["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.hash_password(user.password)
    res = await database["users"].insert_one(
        {"email": user.email, "passwordHash": hashed}
    )
    token = auth.create_access_token(str(res.inserted_id))
    return {"access_token": token}


@app.post("/api/v1/auth/login", response_model=schemas.Token)
async def login(user: schemas.UserCreate):
    database = db.get_db()
    existing = await database["users"].find_one({"email": user.email})
    if not existing:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not auth.verify_password(user.password, existing.get("passwordHash", "")):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token(str(existing["_id"]))
    return {"access_token": token}


@app.post("/api/v1/orders")
async def place_order(
    order: schemas.OrderCreate,
    user: Optional[str] = Depends(get_optional_user_from_token),
):
    database = db.get_db()
    total = sum(item.price * item.quantity for item in order.items)
    doc = {
        "userId": user if user is not None else None,
        "items": [o.dict() for o in order.items],
        "totalAmount": total,
    }
    res = await database["orders"].insert_one(doc)
    return {"id": str(res.inserted_id)}
