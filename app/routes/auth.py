from __future__ import annotations

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.schemas import LoginRequest, MeResponse, TokenResponse, UserCreate, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: sqlite3.Connection = Depends(get_db)) -> UserResponse:
    existing_user = db.execute("SELECT id FROM users WHERE email = ?", (payload.email,)).fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    cursor = db.execute(
        "INSERT INTO users (email, hashed_password, is_active) VALUES (?, ?, 1)",
        (payload.email, get_password_hash(payload.password)),
    )
    user_id = cursor.lastrowid

    db.execute(
        "INSERT INTO profiles (user_id, display_name) VALUES (?, ?)",
        (user_id, payload.display_name),
    )
    db.commit()

    user = db.execute(
        "SELECT id, email, is_active, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()

    return UserResponse(
        id=user["id"],
        email=user["email"],
        is_active=bool(user["is_active"]),
        created_at=user["created_at"],
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: sqlite3.Connection = Depends(get_db)) -> TokenResponse:
    user = db.execute(
        "SELECT email, hashed_password FROM users WHERE email = ?",
        (payload.email,),
    ).fetchone()

    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    return TokenResponse(access_token=create_access_token(user["email"]))


@router.get("/me", response_model=MeResponse)
def read_me(
    current_user: sqlite3.Row = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
) -> MeResponse:
    profile = db.execute(
        "SELECT display_name FROM profiles WHERE user_id = ?",
        (current_user["id"],),
    ).fetchone()

    return MeResponse(
        id=current_user["id"],
        email=current_user["email"],
        is_active=bool(current_user["is_active"]),
        display_name=profile["display_name"] if profile else None,
    )
