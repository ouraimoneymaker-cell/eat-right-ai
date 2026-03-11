from __future__ import annotations

from typing import Dict, List, Optional

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


class ProductSearchResponse(BaseModel):
    total: int
    query: str
    results: List[ProductResponse]


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


class ErrorResponse(BaseModel):
    detail: str


class ProductSearchFilters(BaseModel):
    category: Optional[str] = None
    organic_only: bool = False
    non_gmo_only: bool = False


class FavoriteRequest(BaseModel):
    barcode: str


class FavoriteResponse(BaseModel):
    barcode: str
    created_at: str
    product: Optional[ProductResponse] = None


class LookupEventResponse(BaseModel):
    event_type: str
    lookup_value: str
    metadata_json: Optional[str] = None
    created_at: str


class ReportSummaryResponse(BaseModel):
    total_events: int
    by_type: Dict[str, int]
