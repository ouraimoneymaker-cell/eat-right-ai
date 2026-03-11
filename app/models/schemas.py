from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str


class ProductResponse(BaseModel):
    barcode: str
    name: str
    brand: str
    ingredients: List[str]
    organic: bool
    non_gmo: bool
    certifications: List[str]
    origin_country: str
    category: str


class IngredientInsight(BaseModel):
    ingredient: str
    classification: str
    purpose: str
    concern_level: str
    possible_side_effects: List[str]
    notes: str


class IngredientAnalysisResponse(BaseModel):
    product_name: str
    ingredients: List[IngredientInsight]
    overall_flagged_ingredients: List[str]


class PLUResponse(BaseModel):
    plu: str
    item: str
    organic: bool
    gmo_status: str
    notes: str


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)
    display_name: str | None = Field(default=None, max_length=120)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime


class MeResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    display_name: str | None
