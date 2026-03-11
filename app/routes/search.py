from __future__ import annotations

from typing import List

from fastapi import APIRouter, Query

from app.data.mock_data import PRODUCTS
from app.models.schemas import ProductResponse

router = APIRouter(prefix="/api/search", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def search_products(q: str = Query(..., min_length=2)) -> List[ProductResponse]:
    q_lower = q.strip().lower()
    results: List[ProductResponse] = []

    for product in PRODUCTS.values():
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

    return results
