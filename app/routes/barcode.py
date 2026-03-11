from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import ProductResponse
from app.services.product_service import get_product_by_barcode

router = APIRouter(prefix="/api/barcode", tags=["Products"])


@router.get("/{barcode}", response_model=ProductResponse)
def lookup_barcode(barcode: str) -> ProductResponse:
    product = get_product_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")
    return product
