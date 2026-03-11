from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import log_lookup_event
from app.data.mock_data import PRODUCTS
from app.models.schemas import ProductResponse

router = APIRouter(prefix="/api/barcode", tags=["Products"])


@router.get("/{barcode}", response_model=ProductResponse)
def lookup_barcode(barcode: str) -> ProductResponse:
    normalized = barcode.strip()
    if not normalized.isdigit() or len(normalized) not in {8, 12, 13, 14}:
        raise HTTPException(status_code=422, detail="Barcode must be a numeric UPC/EAN-like code")

    product = PRODUCTS.get(normalized)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")
    log_lookup_event("barcode_lookup", normalized)
    return ProductResponse(**product)
