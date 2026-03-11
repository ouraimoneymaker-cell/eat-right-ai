from __future__ import annotations

from typing import Optional

from app.data.mock_data import PLU_CODES
from app.models.schemas import PLUResponse


def get_plu_item(plu: str) -> Optional[PLUResponse]:
    item = PLU_CODES.get(plu)
    if not item:
        return None
    return PLUResponse(**item)
