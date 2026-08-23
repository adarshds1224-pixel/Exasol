from pathlib import Path

import pandas as pd


base_dir = Path(__file__).resolve().parent
input_path = base_dir / "raw" / "RS_Session_252_AU_590.csv"
output_path = base_dir / "clean" / "national_yearly_trend.csv"


df = pd.read_csv(input_path)
df.columns = ["year", "received", "disposed"]

df["received"] = pd.to_numeric(df["received"], errors="coerce")
df["disposed"] = pd.to_numeric(df["disposed"], errors="coerce")
df["resolution_rate"] = ((df["disposed"] / df["received"]) * 100).round(2)

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("Cleaned national yearly trend table:")
print(df.to_string(index=False))
