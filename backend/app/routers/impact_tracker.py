from pathlib import Path

import pandas as pd
from fastapi import APIRouter


router = APIRouter()


@router.get("/api/impact-tracker")
def get_impact_tracker():
    input_path = (
        Path(__file__).resolve().parents[2]
        / "data-pipeline"
        / "clean"
        / "national_yearly_trend.csv"
    )
    yearly_df = pd.read_csv(input_path)
    yearly_df["year"] = pd.to_numeric(yearly_df["year"], errors="coerce")
    yearly_df = yearly_df.dropna(subset=["year"]).sort_values("year")

    before = yearly_df.iloc[0]
    after = yearly_df.iloc[-1]

    return {
        "before_year": int(before["year"]),
        "after_year": int(after["year"]),
        "before": {
            "received": int(before["received"]),
            "disposed": int(before["disposed"]),
            "resolution_rate": float(before["resolution_rate"]),
        },
        "after": {
            "received": int(after["received"]),
            "disposed": int(after["disposed"]),
            "resolution_rate": float(after["resolution_rate"]),
        },
        "note": "This comparison uses real multi-year national grievance data to illustrate how the Impact Tracker would surface before/after shifts. It is not tied to a specific tracked intervention in this prototype.",
    }
