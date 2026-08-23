from pprint import pprint

import pandas as pd


def load_blind_spots_from_exasol() -> pd.DataFrame:
    from app.services.exasol_service import get_exasol_connection

    conn = get_exasol_connection()

    query = """
        WITH stats AS (
            SELECT
                MIN(resolution_rate) AS min_resolution,
                MAX(resolution_rate) AS max_resolution,
                MIN(pending_gt_3yr) AS min_3yr,
                MAX(pending_gt_3yr) AS max_3yr,
                MIN(pending_gt_1yr_pct) AS min_1yr_pct,
                MAX(pending_gt_1yr_pct) AS max_1yr_pct,
                MIN(total_pending) AS min_pending,
                MAX(total_pending) AS max_pending
            FROM CIVICSAGE.DEPT_KPIS
        ),

        scored AS (
            SELECT
                d.department,
                d.resolution_rate,
                d.pending_gt_3yr,
                d.pending_gt_1yr_pct,
                d.total_pending,

                /* Long-term backlog risk */
                CASE
                    WHEN s.max_3yr = s.min_3yr THEN 0
                    ELSE
                        (
                            (d.pending_gt_3yr - s.min_3yr)
                            / (s.max_3yr - s.min_3yr)
                        ) * 100
                END AS backlog_score,

                /* Percentage of cases aging over one year */
                CASE
                    WHEN s.max_1yr_pct = s.min_1yr_pct THEN 0
                    ELSE
                        (
                            (d.pending_gt_1yr_pct - s.min_1yr_pct)
                            / (s.max_1yr_pct - s.min_1yr_pct)
                        ) * 100
                END AS aging_score,

                /* Lower resolution = higher risk */
                CASE
                    WHEN s.max_resolution = s.min_resolution THEN 0
                    ELSE
                        (
                            (s.max_resolution - d.resolution_rate)
                            / (s.max_resolution - s.min_resolution)
                        ) * 100
                END AS resolution_risk,

                /* Log-scaled volume prevents huge departments dominating */
                CASE
                    WHEN s.max_pending = s.min_pending THEN 0
                    ELSE
                        (
                            LN(1 + d.total_pending)
                            - LN(1 + s.min_pending)
                        )
                        /
                        (
                            LN(1 + s.max_pending)
                            - LN(1 + s.min_pending)
                        ) * 100
                END AS volume_score

            FROM CIVICSAGE.DEPT_KPIS d
            CROSS JOIN stats s
        ),

        final_scores AS (
            SELECT
                department,
                resolution_rate,
                pending_gt_3yr,
                pending_gt_1yr_pct,
                total_pending,

                (
                    backlog_score * 0.35
                    + aging_score * 0.30
                    + resolution_risk * 0.20
                    + volume_score * 0.15
                ) AS raw_risk_score

            FROM scored
        )

        SELECT
            department,
            resolution_rate,
            pending_gt_3yr,
            pending_gt_1yr_pct,
            total_pending,

            ROUND(raw_risk_score, 2) AS risk_score,

            CASE
                WHEN raw_risk_score >= 70 THEN 'HIGH'
                WHEN raw_risk_score >= 40 THEN 'MEDIUM'
                ELSE 'LOW'
            END AS severity

        FROM final_scores

        ORDER BY raw_risk_score DESC
    """

    try:
        df = conn.export_to_pandas(query)
        df.columns = [col.lower() for col in df.columns]
        return df

    finally:
        conn.close()


def detect_blind_spots(df: pd.DataFrame) -> list[dict]:
    results = []

    numeric_columns = [
        "resolution_rate",
        "pending_gt_3yr",
        "pending_gt_1yr_pct",
        "total_pending",
        "risk_score",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    for _, row in df.iterrows():

        department = str(row["department"]).strip()

        if not department:
            continue

        resolution_rate = float(row["resolution_rate"])
        pending_gt_3yr = float(row["pending_gt_3yr"])
        pending_gt_1yr_pct = float(row["pending_gt_1yr_pct"])
        total_pending = float(row["total_pending"])
        risk_score = float(row["risk_score"])
        severity = str(row["severity"]).upper()

        pending_gt_3yr_rounded = int(round(pending_gt_3yr))

        case_word = (
            "case"
            if pending_gt_3yr_rounded == 1
            else "cases"
        )

        indicator_summary = (
            f"{resolution_rate:.2f}% resolution rate, "
            f"{pending_gt_3yr_rounded} {case_word} pending over 3 years, "
            f"{pending_gt_1yr_pct:.2f}% pending over 1 year"
        )

        results.append(
            {
                "department": department,
                "severity": severity,
                "risk_score": round(risk_score, 2),
                "resolution_rate": round(resolution_rate, 2),
                "pending_gt_3yr": pending_gt_3yr_rounded,
                "pending_gt_1yr_pct": round(
                    pending_gt_1yr_pct,
                    2
                ),
                "total_pending": int(round(total_pending)),
                "indicator_summary": indicator_summary,
            }
        )

    return results


def get_all_blind_spots() -> list[dict]:
    df = load_blind_spots_from_exasol()
    return detect_blind_spots(df)


if __name__ == "__main__":
    pprint(
        get_all_blind_spots(),
        sort_dicts=False
    )