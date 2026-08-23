from pathlib import Path

import pandas as pd


base_dir = Path(__file__).resolve().parent
input_path = base_dir / "raw" / "PredictiveAnalytics_2.csv"
output_path = base_dir / "clean" / "monthly_prediction_vs_actual.csv"


df = pd.read_csv(input_path)
df.columns = ["month", "predicted", "actual", "pct_change"]

df["period_date"] = pd.to_datetime(df["month"], format="%b-%y", errors="coerce")
df = df.sort_values("period_date", ascending=True).reset_index(drop=True)

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("Cleaned monthly prediction vs actual table:")
print(df.to_string(index=False))
