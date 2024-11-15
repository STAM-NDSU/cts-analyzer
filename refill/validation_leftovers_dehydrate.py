import os.path
from pathlib import Path
import pandas as pd


projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

for project in projects_list:

    def main(project):
        IO_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(f"{IO_DIR}/{PROJECT}/validation_diff_leftovers_hydrated.csv")
        full_output_file_path = Path(f"{IO_DIR}/{PROJECT}/validation_diff_leftovers.csv")

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            prev = {
                "Datetime": None,
                "Hash": None,
                "Parent": None,
                "Author": None,
                "Commit Msg": None,
                "Filename": None,
                "Removed Test Case": None,
            }

            for index, row in df.iterrows():
                if index == 0:
                    prev = {
                   "Datetime": row["Datetime"],
                   "Hash": row["Hash"],
                    "Parent": row["Parent"],
                    "Author": row["Author"],
                    "Commit Msg": row["Commit Msg"],
                    "Filepath": row["Filepath"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                    }

                else:
                    if row["Hash"] == prev["Hash"]:
                        row["Hash"] = ""
                        row["Parent"] = ""
                        row["Author"] = ""
                        row["Commit Msg"] = ""
                        row["Datetime"] = ""

                        if row["Filename"] == prev["Filename"]:
                            row["Filename"] = ""
                        else:
                            prev["Filename"] = row["Filename"]

                    else:
                        prev["Hash"] = row["Hash"]
                        prev["Parent"] = row["Parent"]
                        prev["Author"] = row["Author"]
                        prev["Datetime"] = row["Datetime"]
                        prev["Commit Msg"] = prev["Commit Msg"]
                        prev["Filename"] = row["Filename"]

            df.to_csv(f"{full_output_file_path}", index=False)
            print(f"Generated {full_output_file_path}")
        else:
            print("ERROR: Files does not exist for project " + project)

    main(project)
