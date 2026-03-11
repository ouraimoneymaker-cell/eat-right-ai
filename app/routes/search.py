from __future__ import annotations

from typing import List

from fastapi import APIRouter, Query

from app.db import log_lookup_event
from app.data.mock_data import PRODUCTS
from app.models.schemas import ProductResponse, ProductSearchResponse

router = APIRouter(prefix="/api/search", tags=["Products"])


@router.get("", response_model=ProductSearchResponse)
def search_products(
    q: str = Query(..., min_length=2, description="Text query for product lookup"),
    category: str | None = Query(None, description="Optional category filter"),
    organic_only: bool = Query(False, description="Only return organic products"),
    non_gmo_only: bool = Query(False, description="Only return non-GMO products"),
    limit: int = Query(25, ge=1, le=100, description="Maximum number of results"),
) -> ProductSearchResponse:
    q_lower = q.strip().lower()
    category_lower = category.strip().lower() if category else None

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

        if q_lower not in haystack:
            continue
        if category_lower and product["category"].lower() != category_lower:
            continue
        if organic_only and not product["organic"]:
            continue
        if non_gmo_only and not product["non_gmo"]:
            continue

        results.append(ProductResponse(**product))
        if len(results) >= limit:
            break

    log_lookup_event("product_search", q.strip(), metadata_json=f"results={len(results)}")
    return ProductSearchResponse(total=len(results), query=q.strip(), results=results)
