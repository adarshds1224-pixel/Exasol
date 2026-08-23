import pandas as pd

from app.services.exasol_service import get_exasol_connection


CSV_PATH = "data-pipeline/clean/dept_kpis_with_severity.csv"
TABLE_NAME = "DEPT_KPIS"


def main():
    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH)

    print(f"Rows found: {len(df)}")

    conn = get_exasol_connection()

    print("Creating schema...")
    conn.execute("CREATE SCHEMA IF NOT EXISTS CIVICSAGE")

    print("Creating table...")
    conn.execute("""
        CREATE OR REPLACE TABLE CIVICSAGE.DEPT_KPIS (
            department VARCHAR(200),
            total_receipts DECIMAL(18,2),
            total_disposal DECIMAL(18,2),
            total_pending DECIMAL(18,2),
            pending_gt_1yr DECIMAL(18,2),
            pending_6to12mo DECIMAL(18,2),
            pending_2to6mo DECIMAL(18,2),
            pending_lt_2mo DECIMAL(18,2),
            resolution_rate DECIMAL(10,2),
            pending_gt_1yr_pct DECIMAL(10,2),
            pending_gt_3yr DECIMAL(18,2)
        )
    """)

    print("Uploading data to Exasol...")

    conn.import_from_pandas(
        df,
        table=("CIVICSAGE", "DEPT_KPIS"),
        import_params={"columns": df.columns.tolist()},
    )

    result = conn.execute(
        "SELECT COUNT(*) AS ROW_COUNT FROM CIVICSAGE.DEPT_KPIS"
    ).fetchone()

    print(f"Rows loaded into Exasol: {result['ROW_COUNT']}")

    print("\nSample data:")
    rows = conn.execute("""
        SELECT
            department,
            resolution_rate,
            pending_gt_3yr,
            pending_gt_1yr_pct
        FROM CIVICSAGE.DEPT_KPIS
        ORDER BY pending_gt_3yr DESC
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(row)

    conn.close()

    print("\n✅ Data successfully loaded into Exasol.")


if __name__ == "__main__":
    main()