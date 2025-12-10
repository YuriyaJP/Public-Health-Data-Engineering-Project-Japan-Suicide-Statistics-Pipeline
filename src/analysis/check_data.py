from pathlib import Path
import pandas as pd

# Get the folder where this script lives
script_dir = Path(__file__).parent

# Correct path to your CSV folder, relative to script
csv_dir = script_dir.parent.parent / "data_raw" / "csvs"

all_columns = set()

for csv_file in csv_dir.glob("*.csv"):
    df = pd.read_csv(csv_file, encoding="utf-8")
    all_columns.update(df.columns)

print("All columns found across CSVs:")
for col in sorted(all_columns):
    print(col)


