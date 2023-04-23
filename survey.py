import os.path
from pathlib import Path
import pandas as pd
import random

INPUT_DIR = "io/outputRevisedLatest"
OUTPUT_FILE = "survey.xlsx"
files = [
    {
        "dir": "commons-lang",
        "filename": "commons-lang-step3_01-01-2000_01-01-2023",
    },
    {
        "dir": "jfreechart",
        "filename": "jfreechart-step3_01-01-2000_01-01-2023",
    },
    {"dir": "pmd", "filename": "pmd-step3_01-01-2000_01-01-2023"},
    {"dir": "gson", "filename": "gson-step3_01-01-2000_01-01-2023"},
    {
        "dir": "commons-math",
        "filename": "commons-math-step3_01-01-2000_01-01-2023",
    },
    {"dir": "cts", "filename": "cts-step3_01-01-2000_01-01-2023"},
]


def parse_files(files):
    return map(lambda file_data: file_data["dir"] + "/" + file_data["filename"] + ".csv", files)


def get_sheet_name(filepath):
    return filepath.split("/")[0]


writer = pd.ExcelWriter(f"{INPUT_DIR}/{OUTPUT_FILE}", engine="xlsxwriter")

for index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{INPUT_DIR}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")
        # print(df.shape)
        df = df.iloc[:, 0:6]
        prev = {
            "DATETIME": None,
            "HASH": None,
            "COMMIT MSG": None,
            "FILENAME": None,
            "REMOVED TEST CASE": None,
            "CONFIDENCE": None,
        }
        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "DATETIME": row["DATETIME"],
                    "HASH": row["HASH"],
                    "COMMIT MSG": row["COMMIT MSG"],
                    "FILENAME": row["FILENAME"],
                    "REMOVED TEST CASE": row["REMOVED TEST CASE"],
                    "CONFIDENCE": row["CONFIDENCE"],
                }

            else:
                if pd.isna(row["DATETIME"]) or pd.isnull(row["DATETIME"]):
                    row["DATETIME"] = prev["DATETIME"]
                else:
                    prev["DATETIME"] = row["DATETIME"]

                if pd.isna(row["HASH"]) or pd.isnull(row["HASH"]):
                    row["HASH"] = prev["HASH"]
                else:
                    prev["HASH"] = row["HASH"]

                if pd.isna(row["COMMIT MSG"]) or pd.isnull(row["COMMIT MSG"]):
                    row["COMMIT MSG"] = prev["COMMIT MSG"]
                else:
                    prev["COMMIT MSG"] = row["COMMIT MSG"]

                if pd.isna(row["FILENAME"]) or pd.isnull(row["FILENAME"]):
                    row["FILENAME"] = prev["FILENAME"]
                else:
                    prev["FILENAME"] = row["FILENAME"]

                if pd.isna(row["REMOVED TEST CASE"]) or pd.isnull(
                    row["REMOVED TEST CASE"]
                ):
                    row["REMOVED TEST CASE"] = prev["REMOVED TEST CASE"]
                else:
                    prev["REMOVED TEST CASE"] = row["REMOVED TEST CASE"]

                if pd.isna(row["CONFIDENCE"]) or pd.isnull(row["CONFIDENCE"]):
                    row["CONFIDENCE"] = prev["CONFIDENCE"]
                else:
                    prev["CONFIDENCE"] = row["CONFIDENCE"]

            # print(row)
        # print(df)

        # Separate LOW testcases
        low_df = df.loc[df["CONFIDENCE"] == "LOW"]
        low_df = low_df.sample(frac = 1)
        if low_df.shape[0] > 20:
            low_candidate_df_index = random.sample(range(0, low_df.shape[0]), 20)
            print(filepath, low_candidate_df_index, low_df.shape[0])
            low_candidate_df = low_df.iloc[low_candidate_df_index]
        else:
            low_candidate_df = low_df
            
        # Seperate HIGH testcases
        high_df = df.loc[df["CONFIDENCE"] == "HIGH"]
        high_df = high_df.sample(frac = 1)
        if high_df.shape[0] > 20:
            high_candidate_df_index = random.sample(range(0, high_df.shape[0]), 20)
            print(filepath, high_candidate_df_index, high_df.shape[0])
            high_candidate_df = high_df.iloc[high_candidate_df_index]
        else:
            high_candidate_df = high_df
            
        # New dataframe consisting of equal no of LOW and HIGH testcases
        new_df = pd.concat([low_candidate_df, high_candidate_df], axis=0)
        new_df["Manual Validation"] = " "
        
        # Option 2: Try with group by 
        # for i, g in df.groupby(['CONFIDENCE']):
        #     print (type(g))

        #     candidate_rows = random.sample(range(0, g.shape[0]), 20)

        #     new_df[i] = df.iloc[candidate_rows]

        # print(new_df)
        # pd.concat([new_df[0], new_df[1]], axis=0)
        
        
        new_df.to_excel(writer, sheet_name=get_sheet_name(filepath), index=False)

writer.close()
