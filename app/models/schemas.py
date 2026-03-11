from __future__ import annotations

from typing import List

from pydantic import BaseModel


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
