import pandas as pd

# ============================================================
# 1. Clean page32 (age breakdown table)
# ============================================================

file1 = "/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_raw/csvs/R6jisatsunojoukyou_page32_table1.csv"
df = pd.read_csv(file1)

# Rename the first column to 年
df.rename(columns={"Unnamed: 0": "年"}, inplace=True)

# Melt to tidy long format
df_long = df.melt(id_vars=["年"], var_name="年齢層", value_name="人数")

# Save cleaned version
df_long.to_csv(
    "/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_processed/R6jisatsunojoukyou_page32_table1_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Saved page32 cleaned table to data_processed/")

# ============================================================
# 2. Load the four other raw tables
# ============================================================

base = "/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_raw/csvs/"

file_page33 = base + "R6jisatsunojoukyou_page33_table1.csv"
file_page31 = base + "R6jisatsunojoukyou_page31_table1.csv"
file_page30_3 = base + "R6jisatsunojoukyou_page30_table3.csv"
file_page30_4 = base + "R6jisatsunojoukyou_page30_table4.csv"

page33 = pd.read_csv(file_page33)
page31 = pd.read_csv(file_page31)
page30_table3 = pd.read_csv(file_page30_3)
page30_table4 = pd.read_csv(file_page30_4)

print("Loaded page33, page31, page30_table3, page30_table4")

# Quick preview to verify columns
print("page33 columns:", list(page33.columns))
print("page31 columns:", list(page31.columns))
print("page30_table3 columns:", list(page30_table3.columns))
print("page30_table4 columns:", list(page30_table4.columns))
