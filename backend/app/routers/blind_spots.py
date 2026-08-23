from fastapi import APIRouter
from pydantic import BaseModel

from app.services.blind_spot_detector import get_all_blind_spots


class BlindSpotItem(BaseModel):
    department: str
    severity: str
    resolution_rate: float
    pending_gt_3yr: float
    pending_gt_1yr_pct: float
    indicator_summary: str


class BlindSpotsResponse(BaseModel):
    blind_spots: list[BlindSpotItem]


router = APIRouter()


@router.get("/api/blind-spots", response_model=BlindSpotsResponse)
def list_blind_spots() -> BlindSpotsResponse:
    return {"blind_spots": get_all_blind_spots()}
