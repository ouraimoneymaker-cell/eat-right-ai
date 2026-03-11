from __future__ import annotations

from typing import Dict, List

from app.data.mock_data import INGREDIENT_FACTS
from app.models.schemas import IngredientAnalysisResponse, IngredientInsight, ProductResponse

DEFAULT_INGREDIENT_FACT: Dict[str, object] = {
    "classification": "Unknown",
    "purpose": "Unknown",
    "concern_level": "unknown",
    "possible_side_effects": [],
    "notes": "No detailed ingredient record yet.",
}


def analyze_product_ingredients(product: ProductResponse) -> IngredientAnalysisResponse:
    ingredient_insights: List[IngredientInsight] = []
    flagged: List[str] = []

    for ingredient in product.ingredients:
        fact = INGREDIENT_FACTS.get(ingredient.strip().lower(), DEFAULT_INGREDIENT_FACT)

        insight = IngredientInsight(
            ingredient=ingredient,
            classification=str(fact["classification"]),
            purpose=str(fact["purpose"]),
            concern_level=str(fact["concern_level"]),
            possible_side_effects=list(fact["possible_side_effects"]),
            notes=str(fact["notes"]),
        )
        ingredient_insights.append(insight)

        if insight.concern_level == "high":
            flagged.append(ingredient)

    return IngredientAnalysisResponse(
        product_name=product.name,
        ingredients=ingredient_insights,
        overall_flagged_ingredients=flagged,
    )
