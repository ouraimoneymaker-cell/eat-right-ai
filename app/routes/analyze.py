from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from app.db import log_lookup_event
from app.data.mock_data import INGREDIENT_FACTS, PRODUCTS
from app.models.schemas import IngredientAnalysisResponse, IngredientInsight

router = APIRouter(prefix="/api/analyze", tags=["Analysis"])


@router.get("/{barcode}", response_model=IngredientAnalysisResponse)
def analyze_product(barcode: str) -> IngredientAnalysisResponse:
    normalized = barcode.strip()
    product = PRODUCTS.get(normalized)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")

    ingredient_insights: List[IngredientInsight] = []
    flagged: List[str] = []

    for ingredient in product["ingredients"]:
        fact = INGREDIENT_FACTS.get(
            ingredient.strip().lower(),
            {
                "classification": "Unknown",
                "purpose": "Unknown",
                "concern_level": "unknown",
                "possible_side_effects": [],
                "notes": "No detailed ingredient record yet.",
            },
        )

        insight = IngredientInsight(
            ingredient=ingredient,
            classification=fact["classification"],
            purpose=fact["purpose"],
            concern_level=fact["concern_level"],
            possible_side_effects=fact["possible_side_effects"],
            notes=fact["notes"],
        )
        ingredient_insights.append(insight)

        if fact["concern_level"] == "high":
            flagged.append(ingredient)

    log_lookup_event("ingredient_analysis", normalized, metadata_json=f"flagged={len(flagged)}")

    return IngredientAnalysisResponse(
        product_name=product["name"],
        ingredients=ingredient_insights,
        overall_flagged_ingredients=flagged,
    )
