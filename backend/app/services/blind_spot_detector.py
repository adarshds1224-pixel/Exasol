from pathlib import Path
from pprint import pprint

import pandas as pd


def load_dept_data() -> pd.DataFrame:
    # TODO: swap this for an Exasol query once the DB connection is ready
    file_path = (
        Path(__file__).resolve().parents[2]
        / "data-pipeline"
        / "clean"
        / "dept_kpis_with_severity.csv"
    )
    return pd.read_csv(file_path)


def detect_blind_spots(df: pd.DataFrame) -> list[dict]:
    working_df = df.copy()

    numeric_cols = ["resolution_rate", "pending_gt_3yr", "pending_gt_1yr_pct"]
    for col in numeric_cols:
        working_df[col] = pd.to_numeric(working_df[col], errors="coerce").fillna(0)

    results = []

    for _, row in working_df.iterrows():
        department = str(row.get("department", "")).strip()
        if not department:
            continue

        resolution_rate = float(row["resolution_rate"])
        pending_gt_3yr = float(row["pending_gt_3yr"])
        pending_gt_1yr_pct = float(row["pending_gt_1yr_pct"])

        severity = None
        if resolution_rate > 90 and pending_gt_3yr > 10:
            severity = "HIGH"
        elif resolution_rate > 85 and pending_gt_1yr_pct > 15:
            severity = "MEDIUM"
        elif resolution_rate > 90 and pending_gt_3yr > 0:
            severity = "LOW"

        if severity is None:
            continue

        pending_gt_3yr_rounded = int(round(pending_gt_3yr))
        case_word = "case" if pending_gt_3yr_rounded == 1 else "cases"
        indicator_summary = (
            f"{resolution_rate}% resolution rate but {pending_gt_3yr_rounded} "
            f"{case_word} pending over 3 years"
        )

        results.append(
            {
                "department": department,
                "severity": severity,
                "resolution_rate": round(resolution_rate, 2),
                "pending_gt_3yr": pending_gt_3yr,
                "pending_gt_1yr_pct": round(pending_gt_1yr_pct, 2),
                "indicator_summary": indicator_summary,
            }
        )

    return results


def get_all_blind_spots() -> list[dict]:
    df = load_dept_data()
    blind_spots = detect_blind_spots(df)

    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    blind_spots.sort(
        key=lambda item: (
            severity_rank.get(item["severity"], 99),
            -float(item.get("pending_gt_3yr", 0)),
        )
    )

    return blind_spots


if __name__ == "__main__":
    pprint(get_all_blind_spots(), sort_dicts=False)
