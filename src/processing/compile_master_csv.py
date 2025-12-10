import pandas as pd
import re

# --- CONFIG ---
csv_file = "52091693-99e4-417b-a87e-8773698fb549.csv"
out_file = "processed_suicide_data.csv"

# --- UTILS ---
def japanese_year_to_western(j_year):
    """Convert Japanese era year to western year."""
    j_year = str(j_year).strip()
    if j_year.startswith("S"):
        return 1925 + int(re.sub(r"\D", "", j_year))
    elif j_year.startswith("H"):
        return 1988 + int(re.sub(r"\D", "", j_year))
    else:
        try:
            return int(j_year)
        except ValueError:
            return None

age_mapping = {
    "～19歳": "0-19",
    "20～29歳": "20-29",
    "30～39歳": "30-39",
    "40～49歳": "40-49",
    "50～59歳": "50-59",
    "60～69歳": "60-69",
    "70～79歳": "70-79",
    "80歳～": "80+",
    "不 詳": "Unknown",
    "不詳": "Unknown"
}

# --- READ CSV ---
# skip initial rows until the header row with age bins is detected
df_raw = pd.read_csv(csv_file, header=None, encoding="utf-8")

# detect header row by searching for "～19歳"
header_row_idx = None
for i, row in df_raw.iterrows():
    if any("～19歳" in str(cell) for cell in row):
        header_row_idx = i
        break

if header_row_idx is None:
    raise ValueError("Could not find header row with age bins.")

# read CSV again with correct header
df = pd.read_csv(csv_file, header=header_row_idx, encoding="utf-8")

# --- CLEAN DATA ---
# Remove completely empty rows
df = df.dropna(how="all")

# Melt age columns
age_cols = [col for col in df.columns if col in age_mapping]
id_vars = [col for col in df.columns if col not in age_cols]

df_melt = df.melt(id_vars=id_vars, value_vars=age_cols, 
                  var_name="age_group", value_name="suicides")

# Normalize age bins
df_melt["age_group"] = df_melt["age_group"].map(age_mapping)

# Clean numeric values
df_melt["suicides"] = df_melt["suicides"].astype(str).str.replace(",", "").str.strip()
df_melt["suicides"] = pd.to_numeric(df_melt["suicides"], errors="coerce")

# Standardize year if needed
if "年" in df_melt.columns or "年度" in df_melt.columns:
    year_col = "年" if "年" in df_melt.columns else "年度"
    df_melt["year"] = df_melt[year_col].apply(japanese_year_to_western)
else:
    df_melt["year"] = df_melt.iloc[:,0].apply(japanese_year_to_western)

# Optional: keep only relevant columns
columns_keep = ["year", "age_group", "suicides"] + [col for col in id_vars if col not in ["年", "年度"]]
df_final = df_melt[columns_keep]

# --- SAVE CLEAN CSV ---
df_final.to_csv(out_file, index=False, encoding="utf-8-sig")
print(f"Processed data saved to {out_file}, {len(df_final)} rows")
