from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import log_lookup_event
from app.data.mock_data import PLU_CODES
from app.models.schemas import PLUResponse

router = APIRouter(prefix="/api/plu", tags=["PLU"])


@router.get("/{plu}", response_model=PLUResponse)
def lookup_plu(plu: str) -> PLUResponse:
    normalized = plu.strip()
    if not normalized.isdigit() or len(normalized) not in {4, 5}:
        raise HTTPException(status_code=422, detail="PLU code must be a 4- or 5-digit numeric code")

    item = PLU_CODES.get(normalized)
    if not item:
        raise HTTPException(status_code=404, detail="PLU code not found")
    log_lookup_event("plu_lookup", normalized)
    return PLUResponse(**item)
