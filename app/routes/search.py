from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.schemas import ProductResponse
from app.services.product_service import search_products

router = APIRouter(prefix="/api/search", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def search_products_route(
    q: str = Query(..., min_length=2, max_length=100),
    organic: Optional[bool] = Query(None),
    non_gmo: Optional[bool] = Query(None),
    category: Optional[str] = Query(None, min_length=2, max_length=50),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0, le=1000),
) -> List[ProductResponse]:
    return search_products(
        q=q,
        organic=organic,
        non_gmo=non_gmo,
        category=category,
        limit=limit,
        offset=offset,
    )
