import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import strip_commit_url
from datetime import datetime
import os
import json


projects_list = [
    # "commons-lang",
    # "commons-math",
    # "pmd",
    # "jfreechart",
    "gson",
    # "joda-time",
    # "cts",
]


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%m/%d/%Y %H:%M:%S")
    d2 = datetime.strptime(d2, "%m/%d/%Y %H:%M:%S")
    return abs((d2 - d1).days)


def change_dateformat(date):
    d1 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
    return datetime.strftime(d1, "%m/%d/%Y %H:%M:%S")


for project in projects_list:

    def main(project):
        VALIDATION_FILES_DIR = "io/validationFiles"
        PROJECTS_DIR = "io/projects"
        PROJECT = project
        full_input_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/validation_diff_done_hydrated.csv"
        )
        stat_version_test_deletions_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_version_test_deletion.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            df = df.iloc[:, 0:11]
            # Parse only deleted tests dataframe
            deleted_tc_df = df[df["Final Results"] == "yes"]

            prev = {
                "Datetime": None,
                "Hash": None,
            }

            results = []
            # Opening JSON file
            tags_selected_json = open(f"{PROJECTS_DIR}/{project}/tags-selected.json")
            tags_selected = json.load(tags_selected_json)
            # Iterating through the json
            for index, tag_info in enumerate(tags_selected):
                tag_info["Datetime"] = change_dateformat(tag_info["Datetime"])
                
                if index == 0:
                    prev["Datetime"] = tag_info["Datetime"]
                    prev["Hash"] = tag_info["Hash"]
                    results.append(
                        [
                            tag_info["Hash"],
                            tag_info["Datetime"],
                            tag_info["Tag"],
                            None,  # total daterange
                            None,  # total commits
                            None,  # total test deletion commits
                            None,  # total deleted tests
                        ]
                    )
                else:
                    cloned_deleted_tc_df = deleted_tc_df.copy(deep=False)
                    # Compute total test deletion commits and deleted tests between datetime of two successive version
                    cloned_deleted_tc_df["Datetime"] = pd.to_datetime(cloned_deleted_tc_df["Datetime"])
                    # greater than the start date and smaller than the end date
                    mask = (cloned_deleted_tc_df["Datetime"] >= prev["Datetime"]) & (
                        cloned_deleted_tc_df["Datetime"] <= tag_info["Datetime"]
                    )
                    cloned_deleted_tc_df = cloned_deleted_tc_df[mask]
                   
                    print(cloned_deleted_tc_df)
                    # Total deleted testcases
                    total_deleted_testcases = cloned_deleted_tc_df.shape[0]
                    # Total test deletion commits
                    total_test_deletion_commits = len(pd.unique(cloned_deleted_tc_df["Hash"]))

                    # Compute the difference in days
                    range = days_between(prev["Datetime"], tag_info["Datetime"])
                    # Compute no of in-between commits
                    cmd = f'git log {prev["Hash"]}...{tag_info["Hash"]} --pretty=oneline | wc -l'
                    current_state = os.getcwd()
                    os.chdir(f"./io/projects/{project}")
                    os.system(cmd + " > tmp")
                    no_of_commits = open("tmp", "r").read().replace("\n", "")
                    os.chdir(current_state)

                    results.append(
                        [
                            tag_info["Hash"],
                            tag_info["Datetime"],
                            tag_info["Tag"],
                            range,  # total daterange
                            no_of_commits,  # total commits
                            total_test_deletion_commits,  # total test deletion commits
                            total_deleted_testcases,  # total deleted tests
                        ]
                    )

                    # Update the previous unique Hash record
                    prev["Datetime"] = tag_info["Datetime"]
                    prev["Hash"] = tag_info["Hash"]

            version_test_deletions_df = pd.DataFrame(
                results,
                columns=[
                    "Hash",
                    "Datetime",
                    "Tag",
                    "Range",
                    "Commits",
                    "Test Deletion Commits",
                    "Total Deleted Tests",
                ],
            )
            version_test_deletions_df.to_csv(
                stat_version_test_deletions_file_path, index=False
            )
            print(f"Generated {stat_version_test_deletions_file_path}")

    main(project)
