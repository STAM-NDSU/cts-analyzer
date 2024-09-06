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
MANUAL_VALIDATION_DIR = "../io/validationFiles/not-obsolete-manual-validation"
OUTPUT_MANUAL_VALIDATION_COMPILATION_DIR = (
    "../io/validationFiles/not-obsolete-manual-validation-compilation-results"
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
    print(
        f"Total `not obsolete` deleted tests: {len(not_obsoltete_testcase_df)}"
    )
    print(
        f"Total TDC with `not obsolete` deleted tests: {len(set(list(not_obsoltete_testcase_df['Hash'])))}"
    )
    
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
        "Deleted Tests": [],
        "Total Deleted Tests": [],
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
        # deleted tests
        deleted_tests = deleted_tests_df["Removed Test Case"].values.tolist()
        data["Deleted Tests"].append(deleted_tests)
        data["Total Deleted Tests"].append(len(deleted_tests))

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
