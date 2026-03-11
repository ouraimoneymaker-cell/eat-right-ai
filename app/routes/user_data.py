from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import require_api_key
from app.data.mock_data import PRODUCTS
from app.db import (
    add_favorite,
    list_favorites,
    list_lookup_events,
    lookup_event_summary,
    remove_favorite,
)
from app.models.schemas import (
    FavoriteRequest,
    FavoriteResponse,
    LookupEventResponse,
    ReportSummaryResponse,
)

router = APIRouter(prefix="/api", tags=["User Data"], dependencies=[Depends(require_api_key)])


@router.get("/history", response_model=List[LookupEventResponse])
def get_history(limit: int = Query(50, ge=1, le=200)) -> List[LookupEventResponse]:
    return [LookupEventResponse(**row) for row in list_lookup_events(limit=limit)]


@router.get("/favorites", response_model=List[FavoriteResponse])
def get_favorites() -> List[FavoriteResponse]:
    rows = list_favorites()
    output: List[FavoriteResponse] = []

    for row in rows:
        product = PRODUCTS.get(row["barcode"])
        output.append(
            FavoriteResponse(
                barcode=row["barcode"],
                created_at=row["created_at"],
                product=product,
            )
        )

    return output


@router.post("/favorites", response_model=FavoriteResponse)
def create_favorite(payload: FavoriteRequest) -> FavoriteResponse:
    barcode = payload.barcode.strip()
    if barcode not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Barcode not found")

    add_favorite(barcode)

    for row in list_favorites():
        if row["barcode"] == barcode:
            return FavoriteResponse(barcode=barcode, created_at=row["created_at"], product=PRODUCTS[barcode])

    raise HTTPException(status_code=500, detail="Favorite write failed")


@router.delete("/favorites/{barcode}")
def delete_favorite(barcode: str) -> dict:
    removed = remove_favorite(barcode.strip())
    if not removed:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"status": "removed", "barcode": barcode.strip()}


@router.get("/reports/summary", response_model=ReportSummaryResponse)
def reports_summary() -> ReportSummaryResponse:
    return ReportSummaryResponse(**lookup_event_summary())
