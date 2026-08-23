from pathlib import Path

import pandas as pd


base_dir = Path(__file__).resolve().parent
severity_path = base_dir / "raw" / "RS-Session-251-AU1712-Table1.csv"
kpis_path = base_dir / "clean" / "dept_kpis.csv"
output_path = base_dir / "clean" / "dept_kpis_with_severity.csv"


severity_df = pd.read_csv(severity_path)
severity_df.columns = ["department", "pending_gt_3yr"]
severity_df["department"] = severity_df["department"].astype("string").str.strip().str.title()
severity_df["pending_gt_3yr"] = pd.to_numeric(severity_df["pending_gt_3yr"], errors="coerce").fillna(0)

# Drop aggregate row if present.
severity_df = severity_df[severity_df["department"] != "Total"]
severity_df = severity_df.dropna(subset=["department"])
severity_df = severity_df[severity_df["department"] != ""]

kpis_df = pd.read_csv(kpis_path)
kpis_df["department"] = kpis_df["department"].astype("string").str.strip().str.title()

kpis_departments = set(kpis_df["department"].dropna())
unmatched_severity = sorted(
    dept for dept in severity_df["department"].dropna().unique() if dept not in kpis_departments
)

merged_df = kpis_df.merge(severity_df, on="department", how="left")
merged_df["pending_gt_3yr"] = pd.to_numeric(merged_df["pending_gt_3yr"], errors="coerce").fillna(0)

output_path.parent.mkdir(parents=True, exist_ok=True)
merged_df.to_csv(output_path, index=False)

print("Departments from severity file with no exact match in dept_kpis.csv:")
if unmatched_severity:
    for dept in unmatched_severity:
        print(f"- {dept}")
else:
    print("- None")

print("\nTop departments by pending_gt_3yr with resolution_rate:")
print(
    merged_df.sort_values(["pending_gt_3yr", "resolution_rate"], ascending=[False, False])
    [["department", "pending_gt_3yr", "resolution_rate"]]
    .head(10)
    .to_string(index=False)
)
