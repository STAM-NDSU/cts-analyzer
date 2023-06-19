# WARNING: Make sure .env is correct set to desired Project
# NOTE: Customized for jodatime

import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import get_full_commit_url, parse_commit_as_hyperlink

IO_DIR = "io/validationFiles4/commons-math"
OUTPUT_FILE = "validation_hydrated"
files = [{"filename": "validated"}]


def parse_files(files):
    return map(lambda file_data: file_data["filename"] + ".csv", files)


for file_index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{IO_DIR}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")

        df = df.iloc[:, 0:12]
        all_data = []

        prev = {
            "Datetime": None,
            "Hash": None,
            "Commit Msg": None,
            "Filename": None,
            "Removed Test Case": None,
            "Confidence": None,
            "Manual Validation": None,
            "Final Results": None,
            "Ajay Manual Validation": None,
            "Suraj Manual Validation": None,
            "Ajay Comments": None,
            "Suraj Comments": None,
        }

        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "Datetime": row["Datetime"],
                    "Commit Msg": row["Commit Msg"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                    "Confidence": row["Confidence"],
                    "Manual Validation": row["Manual Validation"],
                    "Final Results": row["Final Results"],
                    "Ajay Manual Validation": row["Ajay Manual Validation"],
                    "Suraj Manual Validation": row["Suraj Manual Validation"],
                    "Ajay Comments": row["Ajay Comments"],
                    "Suraj Comments": row["Suraj Comments"],
                }
                prev["Hash"] = parse_commit_as_hyperlink(
                    label=row["Hash"], url=get_full_commit_url(row["Hash"])
                )
                row["Hash"] = prev["Hash"]
            else:
                if pd.isna(row["Datetime"]) or pd.isnull(row["Datetime"]):
                    row["Datetime"] = prev["Datetime"]
                else:
                    prev["Datetime"] = row["Datetime"]

                if pd.isna(row["Hash"]) or pd.isnull(row["Hash"]):
                    row["Hash"] = prev["Hash"]
                else:
                    prev["Hash"] = parse_commit_as_hyperlink(
                        label=row["Hash"], url=get_full_commit_url(row["Hash"])
                    )
                    row["Hash"] = prev["Hash"]

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

                # if pd.isna(row["Manual Validation"]) or pd.isnull(row["Manual Validation"]):
                #     row["Manual Validation"] = prev["Manual Validation"]
                # else:
                #     prev["Manual Validation"] = row["Manual Validation"]

                # if pd.isna(row["Ajay Manual Validation"]) or pd.isnull(row["Ajay Manual Validation"]):
                #     row["Ajay Manual Validation"] = prev["Ajay Manual Validation"]
                # else:
                #     prev["Ajay Manual Validation"] = row["Ajay Manual Validation"]

                # if pd.isna(row["Suraj Manual Validation"]) or pd.isnull(row["Suraj Manual Validation"]):
                #     row["Suraj Manual Validation"] = prev["Suraj Manual Validation"]
                # else:
                #     prev["Suraj Manual Validation"] = row["Suraj Manual Validation"]

                # if pd.isna(row["Ajay Comments"]) or pd.isnull(row["Ajay Comments"]):
                #     row["Ajay Comments"] = prev["Ajay Comments"]
                # else:
                #     prev["Ajay Comments"] = row["Ajay Comments"]

                # if pd.isna(row["Suraj Comments"]) or pd.isnull(row["Suraj Comments"]):
                #     row["Suraj Comments"] = prev["Suraj Comments"]
                # else:
                #     prev["Suraj Comments"] = row["Suraj Comments"]

            # new_df = pd.concat([new_df,row])
            data = [
                row["Datetime"],
                row["Hash"],
                row["Commit Msg"],
                row["Filename"],
                row["Removed Test Case"],
                row["Confidence"],
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
                "Commit Msg",
                "Filename",
                "Removed Test Case",
                "Confidence",
                "Manual Validation",
                "Final Results",
                "Ajay Manual Validation",
                "Suraj Manual Validation",
                "Ajay Comments",
                "Suraj Comments",
            ],
        )
        new_df.to_csv(f"{IO_DIR}/{OUTPUT_FILE}.csv", index=False)
        print(f"Generated {IO_DIR}/{OUTPUT_FILE}.csv")
