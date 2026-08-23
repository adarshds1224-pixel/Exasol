from pathlib import Path

import pandas as pd


RAW_DIR = Path(__file__).resolve().parent / "raw"
SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".xlsm", ".xlsb"}


def load_table(file_path: Path) -> pd.DataFrame:
	if file_path.suffix.lower() == ".csv":
		return pd.read_csv(file_path)
	return pd.read_excel(file_path)


def main() -> None:
	if not RAW_DIR.exists():
		print(f"Raw directory not found: {RAW_DIR}")
		return

	files = sorted(path for path in RAW_DIR.iterdir() if path.is_file())

	if not files:
		print(f"No files found in: {RAW_DIR}")
		return

	print(f"Files in {RAW_DIR}:")
	for path in files:
		print(f"- {path.name}")

	print("\n--- Data Preview ---")
	for path in files:
		if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
			continue

		print(f"\nFile: {path.name}")
		try:
			df = load_table(path)
			print(f"Shape: {df.shape}")

			print("Columns and dtypes:")
			for column_name, dtype in df.dtypes.items():
				print(f"  - {column_name}: {dtype}")

			print("First 5 rows:")
			print(df.head(5).to_string(index=False))
		except Exception as exc:
			print(f"Failed to load '{path.name}': {exc}")


if __name__ == "__main__":
	main()
