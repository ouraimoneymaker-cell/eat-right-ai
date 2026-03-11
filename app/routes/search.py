from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query

from app.data.mock_data import PRODUCTS
from app.models.schemas import ProductResponse

router = APIRouter(prefix="/api/search", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def search_products(
    q: str = Query(..., min_length=2, max_length=100),
    organic: Optional[bool] = Query(None),
    non_gmo: Optional[bool] = Query(None),
    category: Optional[str] = Query(None, min_length=2, max_length=50),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0, le=1000),
) -> List[ProductResponse]:
    q_lower = q.strip().lower()
    category_lower = category.strip().lower() if category else None
    results: List[ProductResponse] = []

    for product in PRODUCTS.values():
        if organic is not None and product["organic"] != organic:
            continue

        if non_gmo is not None and product["non_gmo"] != non_gmo:
            continue

        if category_lower and category_lower != product["category"].strip().lower():
            continue

        haystack = " ".join(
            [
                product["name"],
                product["brand"],
                product["category"],
                " ".join(product["ingredients"]),
            ]
        ).lower()

        if q_lower in haystack:
            results.append(ProductResponse(**product))

    return results[offset : offset + limit]
