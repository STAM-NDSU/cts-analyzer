import sys

sys.path.append("../")

import os.path
from pathlib import Path
import pandas as pd


IO_DIR = "../io/validationFiles/"
hydrated_file = "hydrated_rq_2.csv"

projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    "cts",
]

for project in projects_list:
    full_file_path = Path(f"{IO_DIR}/{project}/{hydrated_file}")

    if not os.path.exists(f"{full_file_path}"):
        print(f"{full_file_path} does not exist")
        continue

    with open(full_file_path, "r") as a:
        df = pd.read_csv(f"{full_file_path}")
        prev = {
            "Datetime": None,
            "Hash": None,
            "Author": None,
            "Commit Msg": None,
            "Filepath": None,
            "Filename": None,
            "Removed Test Case": None,
        }

        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "Datetime": row["Datetime"],
                    "Commit Msg": row["Commit Msg"],
                    "Hash": row["Hash"],
                    "Author": row["Author"],
                    "Filepath": row["Filepath"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                }

            else:
                if row["Hash"] == prev["Hash"]:
                    row["Hash"] = ""
                    row["Author"] = ""
                    row["Commit Msg"] = ""
                    row["Datetime"] = ""

                    if row["Filepath"] == prev["Filepath"]:
                        row["Filepath"] = ""
                        row["Filename"] = ""
                    else:
                        prev["Filepath"] = row["Filepath"]
                        prev["Filename"] = row["Filename"]

                else:
                    prev["Hash"] = row["Hash"]
                    prev["Datetime"] = row["Datetime"]
                    prev["Commit Msg"] = prev["Commit Msg"]
                    prev["Filepath"] = row["Filepath"]
                    prev["Filename"] = row["Filename"]

        file_wo = hydrated_file.replace("hydrated_", "")
        df.to_csv(f"{IO_DIR}/{project}/{file_wo}", index=False)
        print(f"Generated {IO_DIR}/{project}/{file_wo}")
