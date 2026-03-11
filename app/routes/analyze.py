from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import IngredientAnalysisResponse
from app.services.analysis_service import analyze_product_ingredients
from app.services.product_service import get_product_by_barcode

router = APIRouter(prefix="/api/analyze", tags=["Analysis"])


@router.get("/{barcode}", response_model=IngredientAnalysisResponse)
def analyze_product(barcode: str) -> IngredientAnalysisResponse:
    product = get_product_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")

    return analyze_product_ingredients(product)
