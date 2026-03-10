from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

APP_NAME = "Eat Right AI"
APP_VERSION = "0.1.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str


class ProductResponse(BaseModel):
    barcode: str
    name: str
    brand: str
    ingredients: List[str]
    organic: bool
    non_gmo: bool
    certifications: List[str]
    origin_country: str
    category: str


class IngredientInsight(BaseModel):
    ingredient: str
    classification: str
    purpose: str
    concern_level: str
    possible_side_effects: List[str]
    notes: str


class IngredientAnalysisResponse(BaseModel):
    product_name: str
    ingredients: List[IngredientInsight]
    overall_flagged_ingredients: List[str]


class PLUResponse(BaseModel):
    plu: str
    item: str
    organic: bool
    gmo_status: str
    notes: str


PRODUCTS: Dict[str, dict] = {
    "012345678905": {
        "barcode": "012345678905",
        "name": "Organic Peanut Butter",
        "brand": "Pure Pantry",
        "ingredients": ["Organic Peanuts", "Sea Salt"],
        "organic": True,
        "non_gmo": True,
        "certifications": ["USDA Organic", "Non-GMO Project"],
        "origin_country": "United States",
        "category": "Nut Butter",
    },
    "070847000103": {
        "barcode": "070847000103",
        "name": "Macaroni & Cheese",
        "brand": "Family Table",
        "ingredients": [
            "Enriched Wheat Flour",
            "Cheese Powder",
            "Whey",
            "Salt",
            "Artificial Flavor",
            "Yellow 5",
            "Yellow 6",
        ],
        "organic": False,
        "non_gmo": False,
        "certifications": [],
        "origin_country": "United States",
        "category": "Packaged Food",
    },
}

PLU_CODES: Dict[str, dict] = {
    "4011": {
        "plu": "4011",
        "item": "Banana",
        "organic": False,
        "gmo_status": "Commonly sold as conventional; not labeled GMO",
        "notes": "Standard conventional banana PLU.",
    },
    "94011": {
        "plu": "94011",
        "item": "Banana",
        "organic": True,
        "gmo_status": "Organic product code",
        "notes": "Organic banana PLU.",
    },
}

INGREDIENT_FACTS: Dict[str, dict] = {
    "organic peanuts": {
        "classification": "Whole food ingredient",
        "purpose": "Primary food ingredient",
        "concern_level": "low",
        "possible_side_effects": ["Peanut allergy risk in sensitive individuals"],
        "notes": "Simple whole-food ingredient.",
    },
    "sea salt": {
        "classification": "Mineral seasoning",
        "purpose": "Flavoring / preservation support",
        "concern_level": "low",
        "possible_side_effects": ["Excess sodium intake if overconsumed"],
        "notes": "Generally low concern in modest amounts.",
    },
    "enriched wheat flour": {
        "classification": "Refined grain",
        "purpose": "Base carbohydrate / texture",
        "concern_level": "medium",
        "possible_side_effects": [
            "May not be suitable for gluten-sensitive individuals",
            "Lower fiber than whole grain alternatives",
        ],
        "notes": "Common processed grain ingredient.",
    },
    "cheese powder": {
        "classification": "Dairy-derived flavor ingredient",
        "purpose": "Flavoring",
        "concern_level": "medium",
        "possible_side_effects": [
            "May affect people with dairy sensitivity",
            "Can contribute sodium and saturated fat",
        ],
        "notes": "Common in packaged cheese products.",
    },
    "whey": {
        "classification": "Milk protein derivative",
        "purpose": "Texture / protein / dairy solids",
        "concern_level": "medium",
        "possible_side_effects": [
            "May affect people with dairy allergy or intolerance",
        ],
        "notes": "Milk-derived ingredient.",
    },
    "salt": {
        "classification": "Mineral seasoning",
        "purpose": "Flavoring / preservation support",
        "concern_level": "medium",
        "possible_side_effects": ["Excess sodium intake if overconsumed"],
        "notes": "Amount matters.",
    },
    "artificial flavor": {
        "classification": "Flavor additive",
        "purpose": "Flavor enhancement",
        "concern_level": "medium",
        "possible_side_effects": [
            "Specific composition often not disclosed on label",
        ],
        "notes": "Broad labeling term; exact source may be unclear.",
    },
    "yellow 5": {
        "classification": "Synthetic color additive",
        "purpose": "Coloring",
        "concern_level": "high",
        "possible_side_effects": [
            "May trigger sensitivity in some individuals",
            "Often avoided by consumers seeking cleaner labels",
        ],
        "notes": "Synthetic dye frequently flagged by ingredient-conscious shoppers.",
    },
    "yellow 6": {
        "classification": "Synthetic color additive",
        "purpose": "Coloring",
        "concern_level": "high",
        "possible_side_effects": [
            "May trigger sensitivity in some individuals",
            "Often avoided by consumers seeking cleaner labels",
        ],
        "notes": "Synthetic dye frequently flagged by ingredient-conscious shoppers.",
    },
}


@app.get("/", tags=["Root"])
def root() -> dict:
    return {
        "message": "Eat Right AI backend is running.",
        "docs": "/docs",
        "version": APP_VERSION,
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=APP_NAME, version=APP_VERSION)


@app.get("/api/barcode/{barcode}", response_model=ProductResponse, tags=["Products"])
def lookup_barcode(barcode: str) -> ProductResponse:
    product = PRODUCTS.get(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")
    return ProductResponse(**product)


@app.get("/api/plu/{plu}", response_model=PLUResponse, tags=["PLU"])
def lookup_plu(plu: str) -> PLUResponse:
    item = PLU_CODES.get(plu)
    if not item:
        raise HTTPException(status_code=404, detail="PLU code not found")
    return PLUResponse(**item)


@app.get("/api/search", response_model=List[ProductResponse], tags=["Products"])
def search_products(q: str = Query(..., min_length=2)) -> List[ProductResponse]:
    q_lower = q.strip().lower()
    results = []

    for product in PRODUCTS.values():
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

    return results


@app.get("/api/analyze/{barcode}", response_model=IngredientAnalysisResponse, tags=["Analysis"])
def analyze_product(barcode: str) -> IngredientAnalysisResponse:
    product = PRODUCTS.get(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Barcode not found")

    ingredient_insights: List[IngredientInsight] = []
    flagged: List[str] = []

    for ingredient in product["ingredients"]:
        fact = INGREDIENT_FACTS.get(
            ingredient.strip().lower(),
            {
                "classification": "Unknown",
                "purpose": "Unknown",
                "concern_level": "unknown",
                "possible_side_effects": [],
                "notes": "No detailed ingredient record yet.",
            },
        )

        insight = IngredientInsight(
            ingredient=ingredient,
            classification=fact["classification"],
            purpose=fact["purpose"],
            concern_level=fact["concern_level"],
            possible_side_effects=fact["possible_side_effects"],
            notes=fact["notes"],
        )
        ingredient_insights.append(insight)

        if fact["concern_level"] == "high":
            flagged.append(ingredient)

    return IngredientAnalysisResponse(
        product_name=product["name"],
        ingredients=ingredient_insights,
        overall_flagged_ingredients=flagged,
    )
