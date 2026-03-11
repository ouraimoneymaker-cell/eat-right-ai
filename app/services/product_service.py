from __future__ import annotations

from typing import List, Optional

from app.data.mock_data import PRODUCTS
from app.models.schemas import ProductResponse


def get_product_by_barcode(barcode: str) -> Optional[ProductResponse]:
    product = PRODUCTS.get(barcode)
    if not product:
        return None
    return ProductResponse(**product)


def search_products(
    q: str,
    organic: Optional[bool],
    non_gmo: Optional[bool],
    category: Optional[str],
    limit: int,
    offset: int,
) -> List[ProductResponse]:
    q_lower = q.strip().lower()
    category_lower = category.strip().lower() if category else None
    results: List[ProductResponse] = []

    for product in PRODUCTS.values():
        if organic is not None and product["organic"] != organic:
            continue

        if non_gmo is not None and product["non_gmo"] != non_gmo:
            continue

        if category_lower and category_lower != product["category"].strip().lower():
            continue

        haystack = " ".join(
            [
                product["name"],
                product["brand"],
                product["category"],
                " ".join(product["ingredients"]),
            ]
        ).lower()

        if q_lower in haystack:
            results.append(ProductResponse(**product))

    return results[offset : offset + limit]
