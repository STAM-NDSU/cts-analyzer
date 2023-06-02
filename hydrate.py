import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

IO_DIR = "io/outputRevisedLatest4"
projects = [
    {
        "project": "pmd",
        "filename": ["pmd-step1", "pmd-step3"],
    },
    # {
    #     "project": "commons-math",
    #     "filename": ["commons-math-step3"],
    # },
    # {
    #     "project": "commons-lang",
    #     "filename": ["commons-lang-step1"],
    # },
    # {
    #     "project": "jodatime",
    #     "filename": ["jodatime-step3"],
    # },
    # {
    #     "project": "gson",
    #     "filename": ["gson-step3"],
    # },
    # {
    #     "project": "jfreechart",
    #     "filename": ["jfreechart-step3"],
    # },
    # {
    #     "project": "joda-time",
    #     "filename": ["joda-time-step3"],
    # },
]


for project in projects:
    for file in project["filename"]:
        full_file_path = Path(f"{IO_DIR}/{project['project']}/{file}.csv")

        if not os.path.exists(f"{full_file_path}"):
            continue

        with open(full_file_path, "r") as a:
            df = pd.read_csv(f"{full_file_path}")

        df = df.iloc[:, 0:7]
        prev = {
            "Datetime": None,
            "Hash": None,
            "Commit Msg": None,
            "Filepath": None,
            "Filename": None,
            "Removed Test Case": None,
            "Check Annot": None,
        }
        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "Datetime": row["Datetime"],
                    "Hash": row["Hash"],
                    "Commit Msg": row["Commit Msg"],
                    "Filepath": row["Filepath"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                    "Check Annot": row["Check Annot"],
                }

                if "Confidence" in row:
                    prev["Confidence"] = row["Confidence"]

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

                if pd.isna(row["Filepath"]) or pd.isnull(row["Filepath"]):
                    row["Filepath"] = prev["Filepath"]
                else:
                    prev["Filepath"] = row["Filepath"]

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

                if pd.isna(row["Check Annot"]) or pd.isnull(row["Check Annot"]):
                    row["Check Annot"] = prev["Check Annot"]
                else:
                    prev["Check Annot"] = row["Check Annot"]

        df.to_csv(f"{IO_DIR}/{project['project']}/hydrated_{file}.csv", index=False)
