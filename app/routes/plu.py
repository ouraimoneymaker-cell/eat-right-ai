from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import PLUResponse
from app.services.plu_service import get_plu_item

router = APIRouter(prefix="/api/plu", tags=["PLU"])


@router.get("/{plu}", response_model=PLUResponse)
def lookup_plu(plu: str) -> PLUResponse:
    item = get_plu_item(plu)
    if not item:
        raise HTTPException(status_code=404, detail="PLU code not found")
    return item
