import sys

sys.path.append("../")

import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import get_full_commit_url, parse_commit_as_hyperlink


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

    def main(project):
        IO_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{IO_DIR}/{PROJECT}/validation_diff_done_hydrated.csv"
        )
        full_output_file_path = Path(f"{IO_DIR}/{PROJECT}/validation_diff_done.csv")

        all_data = []
        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            prev = {}
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
                    "Manual Validation": row["Manual Validation"],
                    "Final Results": row["Final Results"],
                    "Ajay Manual Validation": row["Ajay Manual Validation"],
                    "Suraj Manual Validation": row["Suraj Manual Validation"],
                    "Ajay Comments": row["Ajay Comments"],
                    "Suraj Comments": row["Suraj Comments"],
                }

            else:
                if row["Hash"] == prev["Hash"]:
                    row["Hash"] = ""
                    row["Commit Msg"] = ""
                    row["Author"] = ""
                    row["Datetime"] = ""

                    if row["Filepath"] == prev["Filepath"]:
                        row["Filename"] = ""
                        row["Filepath"] = ""
                    else:
                        prev["Filepath"] = row["Filepath"]
                        prev["Filename"] = row["Filename"]

                else:
                    prev["Hash"] = row["Hash"]
                    prev["Author"] = row["Author"]
                    prev["Datetime"] = row["Datetime"]
                    prev["Commit Msg"] = row["Commit Msg"]
                    prev["Filepath"] = row["Filepath"]
                    prev["Filename"] = row["Filename"]

            data = [
                row["Datetime"],
                row["Hash"],
                row["Author"],
                row["Commit Msg"],
                row["Filepath"],
                row["Filename"],
                row["Removed Test Case"],
                row["Manual Validation"],
                row["Final Results"],
                row["Ajay Manual Validation"],
                row["Suraj Manual Validation"],
                row["Ajay Comments"],
                row["Suraj Comments"],
            ]
            all_data.append(data)

            # new_df.append(row, ignore_index=True)
            # if index == 2 or index == 3:
            #     print(new_df.loc[index])

        new_df = pd.DataFrame(
            data=all_data,
            columns=[
                "Datetime",
                "Hash",
                "Author",
                "Commit Msg",
                "Filepath",
                "Filename",
                "Removed Test Case",
                "Manual Validation",
                "Final Results",
                "Ajay Manual Validation",
                "Suraj Manual Validation",
                "Ajay Comments",
                "Suraj Comments",
            ],
        )
        new_df.to_csv(full_output_file_path, index=False)
        print(f"Generated {full_output_file_path}")

    main(project)
