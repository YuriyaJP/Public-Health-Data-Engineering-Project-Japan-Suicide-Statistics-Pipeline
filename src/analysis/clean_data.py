import pandas as pd
import os

# ========= Helper functions =========

def clean_simple_table(df, name):
    """
    For page31 and page33-like tables: they have unnamed first column and numeric values.
    """
    # Rename first unnamed column to 年
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "年"})

    # Melt into long format
    df_long = df.melt(id_vars=["年"], var_name="category", value_name="value")

    # Save
    out_path = f"/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_processed/{name}_cleaned.csv"
    df_long.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Saved {name} cleaned table to data_processed/")
    return df_long


def clean_problem_table(df, name):
    """
    For tables like page30_table3 and page30_table4: they have Unnamed column + problem types.
    """
    df = df.rename(columns={"Unnamed: 0": "年"})

    df_long = df.melt(id_vars=["年"], 
                      var_name="問題分類", 
                      value_name="人数")

    out_path = f"/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_processed/{name}_cleaned.csv"
    df_long.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Saved {name} cleaned table to data_processed/")
    return df_long


# ========= Load base age table (already working) =========

file_age = "/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_raw/csvs/R6jisatsunojoukyou_page32_table1.csv"
df_age = pd.read_csv(file_age)

df_age.rename(columns={"Unnamed: 0": "年"}, inplace=True)

df_age_long = df_age.melt(id_vars=["年"], var_name="年齢層", value_name="人数")

df_age_long.to_csv(
    "/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_processed/R6jisatsunojoukyou_page32_table1_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Saved page32 cleaned table to data_processed/")


# ========= Load the other raw tables =========

base = "/home/yulia-chekhovska/Public-Health-Data-Engineering-Project-Japan-Suicide-Statistics-Pipeline/data_raw/csvs/"

paths = {
    "page33": base + "R6jisatsunojoukyou_page33_table1.csv",
    "page31": base + "R6jisatsunojoukyou_page31_table1.csv",
    "page30_table3": base + "R6jisatsunojoukyou_page30_table3.csv",
    "page30_table4": base + "R6jisatsunojoukyou_page30_table4.csv",
}

dataframes = {}

for name, path in paths.items():
    df = pd.read_csv(path)
    dataframes[name] = df
    print(f"{name} columns:", list(df.columns))

print("Loaded page33, page31, page30_table3, page30_table4")


# ========= Clean and save them =========

clean_simple_table(dataframes["page33"], "page33")
clean_simple_table(dataframes["page31"], "page31")
clean_problem_table(dataframes["page30_table3"], "page30_table3")
clean_problem_table(dataframes["page30_table4"], "page30_table4")
