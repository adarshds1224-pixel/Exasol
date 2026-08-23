from enum import Enum
from urllib.parse import unquote

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.blind_spot_detector import get_all_blind_spots
from app.services.gemini_investigator import generate_investigation


class ReviewAction(str, Enum):
    accept = "accept"
    modify = "modify"
    reject = "reject"


class InvestigationReviewRequest(BaseModel):
    action: ReviewAction


router = APIRouter()


@router.get("/api/investigations/{department}")
def get_investigation_for_department(department: str):
    decoded_department = unquote(department).strip()
    blind_spots = get_all_blind_spots()

    match = next(
        (
            item
            for item in blind_spots
            if str(item.get("department", "")).strip().lower() == decoded_department.lower()
        ),
        None,
    )

    if match is None:
        raise HTTPException(
            status_code=404,
            detail=f"No blind spot found for department '{decoded_department}'.",
        )

    investigation = generate_investigation(match)

    return {
        **match,
        "hypotheses": investigation.get("hypotheses", []),
        "evidence_gaps": investigation.get("evidence_gaps", []),
        "investigation_brief": investigation.get("investigation_brief", {}),
        "error": investigation.get("error"),
    }


@router.post("/api/investigations/{department}/review")
def review_investigation(department: str, payload: InvestigationReviewRequest):
    decoded_department = unquote(department).strip()
    action = payload.action.value

    if action.endswith("e"):
        action_past = f"{action}d"
    else:
        action_past = f"{action}ed"

    return {
        "department": decoded_department,
        "action": action,
        "status": "recorded",
        "message": f"Investigation {action_past} - routed to administrator queue",
    }
