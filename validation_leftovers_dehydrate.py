import os.path
from pathlib import Path
import pandas as pd

IO_DIR = "io/validationFiles4"
PROJECT = "cts"
OUTPUT_FILE = "validation_diff_leftovers"
files = [{"filename": "validation_diff_leftovers_hydrated"}]


def parse_files(files):
    return map(lambda file_data: file_data["filename"] + ".csv", files)


for file_index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{IO_DIR}/{PROJECT}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")

        df = df.iloc[:, 0:6]
        prev = {
            "Datetime": None,
            "Hash": None,
            "Commit Msg": None,
            "Filename": None,
            "Removed Test Case": None,
        }

        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "Datetime": row["Datetime"],
                    "Commit Msg": row["Commit Msg"],
                    "Hash": row["Hash"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                }

            else:
                if row["Hash"] == prev["Hash"]:
                    row["Hash"] = ""
                    row["Commit Msg"] = ""
                    row["Datetime"] = ""

                    if row["Filename"] == prev["Filename"]:
                        row["Filename"] = ""
                    else:
                        prev["Filename"] = row["Filename"]

                else:
                    prev["Hash"] = row["Hash"]
                    prev["Datetime"] = row["Datetime"]
                    prev["Commit Msg"] = prev["Commit Msg"]

                    prev["Filename"] = row["Filename"]

        df.to_csv(f"{IO_DIR}/{PROJECT}/{OUTPUT_FILE}.csv", index=False)
