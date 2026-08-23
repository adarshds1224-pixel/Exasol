from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.routers.blind_spots import router as blind_spots_router
from app.routers.dashboard import router as dashboard_router
from app.routers.evidence import router as evidence_router
from app.routers.impact_tracker import router as impact_router
from app.routers.investigations import router as investigations_router
from app.routes.reality_check import router as reality_check_router

app = FastAPI(title=Settings.APP_NAME, version=Settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(reality_check_router)
app.include_router(blind_spots_router)
app.include_router(investigations_router)
app.include_router(evidence_router)
app.include_router(impact_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "CivicSage backend",
        "app": Settings.APP_NAME,
    }


@app.get("/")
def root():
    return {
        "service": Settings.APP_NAME,
        "status": "running",
    }
