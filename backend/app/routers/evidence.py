from fastapi import APIRouter


router = APIRouter()


@router.get("/api/evidence")
def list_evidence():
    return {
        "evidence_sources": [
            {
                "source_name": "Dept-wise Receipt & Disposal Statistics",
                "type": "KPI Data",
                "origin": "Rajya Sabha / DARPG official records (Jan 2016 - Nov 2019)",
                "verified": True,
            },
            {
                "source_name": "Pending Cases Beyond 3 Years",
                "type": "Severity Signal",
                "origin": "Rajya Sabha Session 251 unstarred question data",
                "verified": True,
            },
            {
                "source_name": "National Yearly Grievance Trend",
                "type": "Historical Data",
                "origin": "Rajya Sabha Session 252 unstarred question data",
                "verified": True,
            },
            {
                "source_name": "Monthly Prediction vs Actual",
                "type": "Operational Signal",
                "origin": "Prototype predictive model output (synthetic forecast, compared against 2025 actuals)",
                "verified": False,
            },
        ]
    }
