from pathlib import Path

import pandas as pd


input_path = Path(__file__).resolve().parent / "raw" / "Dept_stat_receipt_disposal_010112019.csv"
output_path = Path(__file__).resolve().parent / "clean" / "dept_kpis.csv"


df = pd.read_csv(input_path)

# Rename columns to the required standardized names.
df.columns = [
    "department",
    "total_receipts",
    "total_disposal",
    "total_pending",
    "pending_gt_1yr",
    "pending_6to12mo",
    "pending_2to6mo",
    "pending_lt_2mo",
]

# Normalize department names.
df["department"] = df["department"].astype("string").str.strip().str.title()

# Ensure numeric columns are numeric before calculations and filtering.
numeric_cols = [
    "total_receipts",
    "total_disposal",
    "total_pending",
    "pending_gt_1yr",
    "pending_6to12mo",
    "pending_2to6mo",
    "pending_lt_2mo",
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

rows_before = len(df)

# Compute requested KPI columns.
df["resolution_rate"] = ((df["total_disposal"] / df["total_receipts"]) * 100).round(2)
df["pending_gt_1yr_pct"] = (
    (df["pending_gt_1yr"] / df["total_pending"].replace(0, pd.NA)) * 100
).round(2).fillna(0)

# Drop rows with missing department or zero receipts.
df = df.dropna(subset=["department"])
df = df[df["department"] != ""]
df = df[df["total_receipts"] != 0]

rows_after = len(df)

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Rows before cleaning: {rows_before}")
print(f"Rows after cleaning: {rows_after}")

print("Top 5 departments by resolution_rate:")
print(
    df.sort_values("resolution_rate", ascending=False)
    [["department", "resolution_rate"]]
    .head(5)
    .to_string(index=False)
)
