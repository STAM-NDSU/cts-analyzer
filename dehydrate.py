import os.path
from pathlib import Path
import pandas as pd


IO_DIR = "io/artifacts"
projects = [
    {
        "project": "pmd",
        "filename": [
            "hydrated_pmd-step1",
            "hydrated_pmd-step11",
            "hydrated_pmd-step2",
            "hydrated_pmd-step3",
        ],
    },
    {
        "project": "commons-math",
        "filename": [
            "hydrated_commons-math-step1",
            "hydrated_commons-math-step11",
            "hydrated_commons-math-step2",
            "hydrated_commons-math-step3",
        ],
    },
    {
        "project": "commons-lang",
        "filename": [
            "hydrated_commons-lang-step1",
            "hydrated_commons-lang-step11",
            "hydrated_commons-lang-step2",
            "hydrated_commons-lang-step3",
        ],
    },
    {
        "project": "joda-time",
        "filename": [
            "hydrated_joda-time-step1",
            "hydrated_joda-time-step11",
            "hydrated_joda-time-step2",
            "hydrated_joda-time-step3",
        ],
    },
    {
        "project": "gson",
        "filename": [
            "hydrated_gson-step1",
            "hydrated_gson-step11",
            "hydrated_gson-step2",
            "hydrated_gson-step3",
        ],
    },
    {
        "project": "jfreechart",
        "filename": [
            "hydrated_jfreechart-step1",
            "hydrated_jfreechart-step11",
            "hydrated_jfreechart-step2",
            "hydrated_jfreechart-step3",
        ],
    },
    {
        "project": "joda-time",
        "filename": [
            "hydrated_joda-time-step1",
            "hydrated_joda-time-step11",
            "hydrated_joda-time-step2",
            "hydrated_joda-time-step3",
        ],
    },
    {
        "project": "cts",
        "filename": [
            "hydrated_cts-step1",
            "hydrated_cts-step11",
            "hydrated_cts-step2",
            "hydrated_cts-step3",
        ],
    },
]


for project in projects:
    for file in project["filename"]:
        full_file_path = Path(f"{IO_DIR}/{project['project']}/{file}.csv")

        if not os.path.exists(f"{full_file_path}"):
            print(f"{full_file_path} does not exist")
            continue

        with open(full_file_path, "r") as a:
            df = pd.read_csv(f"{full_file_path}")

        if "Check Annot" in df:
            df = df.iloc[:, 0:7]
        else:
            df = df.iloc[:, 0:6]

        prev = {
            "Datetime": None,
            "Hash": None,
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
                    "Filepath": row["Filepath"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                }

            else:
                if row["Hash"] == prev["Hash"]:
                    row["Hash"] = ""
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

        file_wo = file.replace("hydrated_", "")
        df.to_csv(f"{IO_DIR}/{project['project']}/{file_wo}.csv", index=False)
        print(f"Generated {IO_DIR}/{project['project']}/{file_wo}.csv")
