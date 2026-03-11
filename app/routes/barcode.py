from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.data.mock_data import PRODUCTS
from app.models.schemas import ProductResponse

router = APIRouter(prefix="/api/barcode", tags=["Products"])


@router.get("/{barcode}", response_model=ProductResponse)
def lookup_barcode(barcode: str) -> ProductResponse:
    product = PRODUCTS.get(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")
    return ProductResponse(**product)
