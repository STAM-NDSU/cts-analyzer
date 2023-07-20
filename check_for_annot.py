import csv
from analyzer.helpers import export_to_csv
from pathlib import Path
import os

DIR = "io/artifacts"
projects = [
    {
        "project": "pmd",
        "filename": ["pmd-step1"],
    },
    {
        "project": "commons-math",
        "filename": ["commons-math-step1"],
    },
    {
        "project": "commons-lang",
        "filename": ["commons-lang-step1"],
    },
    {
        "project": "jodatime",
        "filename": ["jodatime-step1"],
    },
    {
        "project": "gson",
        "filename": ["gson-step1"],
    },
    {
        "project": "jfreechart",
        "filename": ["jfreechart-step1"],
    },
    {
        "project": "joda-time",
        "filename": ["joda-time-step1"],
    },
]


for project in projects:
    for file in project["filename"]:
        full_file_path = Path(f"{DIR}/{project['project']}/{file}.csv")
        print(full_file_path)
        if not os.path.exists(f"{full_file_path}"):
            continue

        with open(full_file_path, "r") as a:
            full_file_path = list(csv.reader(a, delimiter=","))

            alter = []
            unique = []
            for new_testcase_data in full_file_path:
                if new_testcase_data[6] == "check":
                    if new_testcase_data[1] not in unique:
                        unique.append(new_testcase_data[1])
                        alter.append([new_testcase_data[1]])

            export_to_csv(
                headers=["Hash"],
                records=alter,
                filename="check_annotation",
                dir=f"{DIR}/{project['project']}",
            )
