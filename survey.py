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
    return map(
        lambda file_data: file_data["dir"] + "/" + file_data["filename"] + ".csv", files
    )


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
            "Datetime": None,
            "Hash": None,
            "Commit Msg": None,
            "Filename": None,
            "Removed Test Case": None,
            "Confidence": None,
        }
        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "Datetime": row["Datetime"],
                    "Hash": row["Hash"],
                    "Commit Msg": row["Commit Msg"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                    "Confidence": row["Confidence"],
                }

            else:
                if pd.isna(row["Datetime"]) or pd.isnull(row["Datetime"]):
                    row["Datetime"] = prev["Datetime"]
                else:
                    prev["Datetime"] = row["Datetime"]

                if pd.isna(row["Hash"]) or pd.isnull(row["Hash"]):
                    row["Hash"] = prev["Hash"]
                else:
                    prev["Hash"] = row["Hash"]

                if pd.isna(row["Commit Msg"]) or pd.isnull(row["Commit Msg"]):
                    row["Commit Msg"] = prev["Commit Msg"]
                else:
                    prev["Commit Msg"] = row["Commit Msg"]

                if pd.isna(row["Filename"]) or pd.isnull(row["Filename"]):
                    row["Filename"] = prev["Filename"]
                else:
                    prev["Filename"] = row["Filename"]

                if pd.isna(row["Removed Test Case"]) or pd.isnull(
                    row["Removed Test Case"]
                ):
                    row["Removed Test Case"] = prev["Removed Test Case"]
                else:
                    prev["Removed Test Case"] = row["Removed Test Case"]

                if pd.isna(row["Confidence"]) or pd.isnull(row["Confidence"]):
                    row["Confidence"] = prev["Confidence"]
                else:
                    prev["Confidence"] = row["Confidence"]

            # print(row)
        # print(df)

        # Separate LOW testcases
        low_df = df.loc[df["Confidence"] == "LOW"]
        low_df = low_df.sample(frac=1)
        if low_df.shape[0] > 20:
            low_candidate_df_index = random.sample(range(0, low_df.shape[0]), 20)
            print(filepath, low_candidate_df_index, low_df.shape[0])
            low_candidate_df = low_df.iloc[low_candidate_df_index]
        else:
            low_candidate_df = low_df

        # Seperate HIGH testcases
        high_df = df.loc[df["Confidence"] == "HIGH"]
        high_df = high_df.sample(frac=1)
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
        # for i, g in df.groupby(['Confidence']):
        #     print (type(g))

        #     candidate_rows = random.sample(range(0, g.shape[0]), 20)

        #     new_df[i] = df.iloc[candidate_rows]

        # print(new_df)
        # pd.concat([new_df[0], new_df[1]], axis=0)

        new_df.to_excel(writer, sheet_name=get_sheet_name(filepath), index=False)

writer.close()
