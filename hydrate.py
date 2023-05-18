import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

IO_DIR = "io/outputRevisedLatest2"
PROJECT = "commons-lang"

""" Step 1"""
OUTPUT_FILE = "commons-lang_hydrated_step"
files = [
    {
        "filename": "commons-lang-step1_01-01-2000_01-01-2023",
    },
    {
        "filename": "commons-lang-step2_01-01-2000_01-01-2023",
    },
    {
        "filename": "commons-lang-step3_01-01-2000_01-01-2023",
    },
]


def parse_files(files):
    return map(lambda file_data: file_data["filename"] + ".csv", files)


for file_index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{IO_DIR}/{PROJECT}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")

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
        df.to_csv(f"{IO_DIR}/{PROJECT}/{OUTPUT_FILE}_{file_index+1}.csv", index=False)
