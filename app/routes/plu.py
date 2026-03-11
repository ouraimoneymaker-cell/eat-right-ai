from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.data.mock_data import PLU_CODES
from app.models.schemas import PLUResponse

router = APIRouter(prefix="/api/plu", tags=["PLU"])


@router.get("/{plu}", response_model=PLUResponse)
def lookup_plu(plu: str) -> PLUResponse:
    item = PLU_CODES.get(plu)
    if not item:
        raise HTTPException(status_code=404, detail="PLU code not found")
    return PLUResponse(**item)
