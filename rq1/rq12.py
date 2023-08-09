"""
Computes test-deletion stat across projects version
"""
import sys

sys.path.append("../")

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
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%m/%d/%Y %H:%M:%S")
    d2 = datetime.strptime(d2, "%m/%d/%Y %H:%M:%S")
    return abs((d2 - d1).days)


def change_dateformat(date):
    d1 = datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
    return datetime.strftime(d1, "%m/%d/%Y %H:%M:%S")


def prettify_tag(project, tag):
    # pretify tag
    tag = tag.split("/")[-1].replace("^{}", "").replace("v", "")
    tag = tag.replace("LANG_", "").replace("commons-lang-", "")  # commons-lang
    tag = tag.replace("_", ".")
    tag = (
        tag.replace("gson-", "")
        .replace("parent-", "")
        .replace("android-", "")
        .replace("-beta1-RC1", "")
        .replace("-beta", "")
    )  # gson
    tag = tag.replace("MATH.", "").replace("commons-math-", "")  # commons-math
    tag = (
        tag.replace("platform-", "")
        .replace("android-platform-", "")
        .replace(".r1", "")
        .replace("0.0", "0")
    )
    if project == "cts":
        tag = tag.replace("1.0", "1")  # cts
    elif project == "joda-time":
        tag = tag.replace("6.0", "6").replace("11.0", "11").replace("12.0", "12")
    elif project == "pmd":
        tag = tag.replace(".0", "")
    elif project == "jfreechart":
        tag = tag.replace("1.0.18", "1.0")
        tag = tag.replace("5.0", "5")
    elif project == "gson":
        tag = tag.replace("8.0", "8").replace("9.0", "9")
    elif project == "commons-lang":
        tag = tag.replace("3.12.0", "3.12")

    if not "." in tag:
        tag = tag + ".0"
    return tag

def hello():
    global projects_list 
    for project in projects_list:

        def main(project):
            print(project)
            print("-----------------")
            VALIDATION_FILES_DIR = "../io/validationFiles"
            PROJECTS_DIR = "../io/projects"
            PROJECT = project
            full_input_file_path = Path(
                f"{VALIDATION_FILES_DIR}/{PROJECT}/validation_diff_done_hydrated.csv"
            )
            stat_version_test_deletions_file_path = Path(
                f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_version_test_deletion.csv"
            )

            if os.path.exists(f"{full_input_file_path}"):
                df = pd.read_csv(f"{full_input_file_path}")
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

                tags_selected = list(
                    filter(
                        lambda each: "Include" not in each.keys()
                        or each["Include"] == True,
                        tags_selected,
                    )
                )
                print(tags_selected)
                # Iterating through the tags json
                for index, tag_info in enumerate(tags_selected):
                    tag_info["Datetime"] = change_dateformat(tag_info["Datetime"])
                    tag = prettify_tag(project, tag_info["Tag"])
                    if index == 0:
                        prev["Datetime"] = tag_info["Datetime"]
                        prev["Hash"] = tag_info["Hash"]
                        # Ignore starting hash
                        # results.append(
                        #     [
                        #         tag_info["Hash"],
                        #         tag_info["Datetime"],
                        #         tag,
                        #         None,  # total daterange
                        #         None,  # total commits
                        #         None,  # total test deletion commits
                        #         None,  # total deleted tests
                        #     ]
                        # )
                        pass
                    else:
                        cloned_deleted_tc_df = deleted_tc_df.copy(deep=False)
                        # Compute total test deletion commits and deleted tests between datetime of two successive version
                        cloned_deleted_tc_df["Datetime"] = pd.to_datetime(
                            cloned_deleted_tc_df["Datetime"]
                        )
                        # greater than the start date and smaller than the end date
                        mask = (cloned_deleted_tc_df["Datetime"] >= prev["Datetime"]) & (
                            cloned_deleted_tc_df["Datetime"] <= tag_info["Datetime"]
                        )
                        cloned_deleted_tc_df = cloned_deleted_tc_df[mask]

                        print(cloned_deleted_tc_df)
                        # Total deleted testcases
                        total_deleted_testcases = cloned_deleted_tc_df.shape[0]
                        # Total test deletion commits
                        total_test_deletion_commits = len(
                            pd.unique(cloned_deleted_tc_df["Hash"])
                        )

                        # Compute the difference in days
                        range = days_between(prev["Datetime"], tag_info["Datetime"])
                        # Compute no of in-between commits
                        cmd = f'git log {prev["Hash"]}...{tag_info["Hash"]} --pretty=oneline | wc -l'
                        current_state = os.getcwd()
                        os.chdir(f"../io/projects/{project}")
                        os.system(cmd + " > tmp")
                        no_of_commits = open("tmp", "r").read().replace("\n", "")
                        os.chdir(current_state)

                        results.append(
                            [
                                tag_info["Hash"],
                                tag_info["Datetime"],
                                tag,
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
                print("======================================================")

        main(project)

if __name__ == 'main':
    hello()