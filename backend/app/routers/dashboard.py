from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from app.services.blind_spot_detector import get_all_blind_spots, load_dept_data


router = APIRouter()


@router.get("/api/dashboard")
def get_dashboard():
    blind_spots = get_all_blind_spots()
    full_dept_df = load_dept_data()

    active_blind_spots = len(blind_spots)
    high_severity_count = sum(1 for item in blind_spots if item.get("severity") == "HIGH")
    cases_analyzed = len(full_dept_df)

    data_pipeline_clean_dir = Path(__file__).resolve().parents[2] / "data-pipeline" / "clean"

    yearly_path = data_pipeline_clean_dir / "national_yearly_trend.csv"
    monthly_path = data_pipeline_clean_dir / "monthly_prediction_vs_actual.csv"

    yearly_df = pd.read_csv(yearly_path)
    monthly_df = pd.read_csv(monthly_path)

    yearly_trend = (
        yearly_df[["year", "received", "disposed", "resolution_rate"]]
        .to_dict(orient="records")
    )
    monthly_prediction = (
        monthly_df[["month", "predicted", "actual", "pct_change"]]
        .to_dict(orient="records")
    )

    return {
        "active_blind_spots": active_blind_spots,
        "high_severity_count": high_severity_count,
        "cases_analyzed": cases_analyzed,
        "top_blind_spots": blind_spots[:3],
        "yearly_trend": yearly_trend,
        "monthly_prediction": monthly_prediction,
    }
