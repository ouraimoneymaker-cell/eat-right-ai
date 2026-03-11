from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import HealthResponse
from app.routes.analyze import router as analyze_router
from app.routes.barcode import router as barcode_router
from app.routes.plu import router as plu_router
from app.routes.search import router as search_router

APP_NAME = "Eat Right AI"
APP_VERSION = "0.1.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


app.include_router(barcode_router)
app.include_router(plu_router)
app.include_router(search_router)
app.include_router(analyze_router)
