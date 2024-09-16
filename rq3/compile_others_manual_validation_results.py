"""
Compiles results obtained after manual validation of `not-obsolete` tests.

Output:
Parent commits of test deletion commit with `not obsolete` delete tests. We compute test coverage loss and mutation loss after removing 
such tests from repository instance of parent test deleteion commits. 
"""

import json
from functools import reduce
from math import fsum
import pandas as pd
import os
from pathlib import Path

VALIDATION_DIR = "../io/validationFiles"
MANUAL_VALIDATION_DIR = "../io/validationFiles/others-manual-validation"
OUTPUT_MANUAL_VALIDATION_COMPILATION_DIR = (
    "../io/validationFiles/not-obsolete-parent-commits"
)
NOT_OBSOLETE_DIR = (
    "../io/validationFiles/not-obsolete"
)

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
]


def get_not_obsolete_test_deletion_commits_df(project):
    manual_validation_file = Path(f"{MANUAL_VALIDATION_DIR}/{project}.csv")
    if not os.path.exists(f"{manual_validation_file}"):
        print(
            "Error: path does not exit -> ",
            manual_validation_file,
        )
        exit()

    df = pd.read_csv(manual_validation_file)
    not_obsoltete_testcase_df = df[df["Final Type"] == "not obsolete"]
    print(f"Total `not obsolete` deleted tests: {len(not_obsoltete_testcase_df)}")
    print(
        f"Total TDC with `not obsolete` deleted tests: {len(set(list(not_obsoltete_testcase_df['Hash'])))}"
    )

    # Place those tests into not-obsolete folder
    temp_df = not_obsoltete_testcase_df.copy()
    if not os.path.exists(NOT_OBSOLETE_DIR):
        os.mkdir(NOT_OBSOLETE_DIR)
    temp_df.to_csv(f"{NOT_OBSOLETE_DIR}/{project}.csv", index=False)
    return not_obsoltete_testcase_df


def get_not_obsolete_test_deletion_commits_parent_commits_list(
    not_obsoltete_testcase_df,
):
    parent_commits_list = list(set(list(not_obsoltete_testcase_df["Parent"])))
    print(
        f"Total parent commits of TDC with `not obsolete` deleted tests: {len(parent_commits_list)}"
    )
    return parent_commits_list


def export(parent_commits_list, not_obsolete_deleted_tests):
    """Export brief summary about parent commits of TDC with `not obsolete` tests"""
    data = {
        "Child Commit Recent Date": [],
        "Parent": [],
        "Hash": [],
        "Deleted Tests Filepath": [],
        "Deleted Tests": [],
        "Deleted Tests Location": [],
        "Deleted Tests With Whole File": [],
        "Total Deleted Tests": [],
        "Total Deleted Tests With Whole File": [],
    }
    for parent_commit in parent_commits_list:
        deleted_tests_df = not_obsolete_deleted_tests[
            not_obsolete_deleted_tests["Parent"] == parent_commit
        ]
        datetime = deleted_tests_df["Datetime"].max()
        data["Child Commit Recent Date"].append(datetime)
        data["Parent"].append(parent_commit)
        # child tdcs
        child_tdcs = list(set(deleted_tests_df["Hash"].values.tolist()))
        data["Hash"].append(child_tdcs)
        # deleted tests filepath
        deleted_tests_filepath = list(set(deleted_tests_df["Filepath"].values.tolist()))
        data["Deleted Tests Filepath"].append(deleted_tests_filepath)
        # deleted tests
        deleted_tests = deleted_tests_df["Removed Test Case"].values.tolist()
        data["Deleted Tests"].append(deleted_tests)
        # deleted tests location
        deleted_tests_location = {}
        for filepath in deleted_tests_filepath:
            filepath_deleted_tests_df = deleted_tests_df[
                (deleted_tests_df["Filepath"] == filepath)
                & (deleted_tests_df["Parent"] == parent_commit)
            ]
            filepath_deleted_tests = filepath_deleted_tests_df[
                "Removed Test Case"
            ].values.tolist()
            deleted_tests_location[filepath] = filepath_deleted_tests
        data["Deleted Tests Location"].append(deleted_tests_location)
        # deleted with whole file
        deleted_tc_with_whole_file_df = deleted_tests_df[
            deleted_tests_df["Deleted With Whole File"] == "yes"
        ]
        deleted_with_whole_file = {
            "Total File": len(list(set(deleted_tc_with_whole_file_df["Filepath"].values.tolist()))),
            "Total Tests": len(deleted_tc_with_whole_file_df),
            "Files": list(set(deleted_tc_with_whole_file_df["Filepath"].values.tolist())),
        }
        data["Deleted Tests With Whole File"].append(deleted_with_whole_file)
        # Total deleted tests
        data["Total Deleted Tests"].append(len(deleted_tests))
        data["Total Deleted Tests With Whole File"].append(
            deleted_with_whole_file["Total Tests"]
        )

    df = pd.DataFrame(data)
    df["Child Commit Recent Date"] = pd.to_datetime(
        df["Child Commit Recent Date"], errors="coerce"
    )
    df.sort_values(by=["Child Commit Recent Date"], inplace=True)
    if not os.path.exists(OUTPUT_MANUAL_VALIDATION_COMPILATION_DIR):
        os.mkdir(OUTPUT_MANUAL_VALIDATION_COMPILATION_DIR)
    df.to_csv(f"{OUTPUT_MANUAL_VALIDATION_COMPILATION_DIR}/{project}.csv", index=False)


for project in projects_list:
    print(project)
    print("--------")
    not_obsolete_tdc_df = get_not_obsolete_test_deletion_commits_df(project)
    not_obsolete_tdc_parent_commits_list = (
        get_not_obsolete_test_deletion_commits_parent_commits_list(not_obsolete_tdc_df)
    )

    export(not_obsolete_tdc_parent_commits_list, not_obsolete_tdc_df)
    print("----*******----")
