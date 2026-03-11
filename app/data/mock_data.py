from __future__ import annotations

from typing import Dict

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
