import sys

sys.path.append("../")
# Redirect console ouput to a file
sys.stdout = open("../stats/all_repos_deleted_tests_percentage_stat2.txt", "w")

import os
from pathlib import Path
import javalang
from typing import Optional, List
from analyzer.pattern import Pattern
import re
from analyzer.utils import (
    cleanup_function_prototype,
    get_function_name_from_prototype_with_space_before,
    get_test_function_name_from_prototype,
    strip_commit_url,
)
import pandas as pd
import numpy as np


# Customized
def compute_testcases_javaparser(code) -> Optional[List[str]]:
    """
    Return the list of testcases (begin with test or annotated) in the before source code testcases using javaparser
    :param code: file code content
    """
    if not code:
        return

    try:
        tree = javalang.parse.parse(code)
        methods = tree.filter(javalang.tree.MethodDeclaration)

        def filter_testcases(method):
            path, node = method
            if "public" not in node.modifiers:
                return False

            if node.return_type is not None:
                return False

            testcase_name = re.search("test([a-zA-Z0-9_]+)", node.name)
            if testcase_name:
                return True
            else:
                for each in node.annotations:
                    if each.name == "Test":
                        return True

            return False

        testcases_methods = filter(filter_testcases, methods)

        testcases = []
        for path, node in testcases_methods:
            testcases.append(node.name)

        return testcases
    except:
        return None


def compute_testcases_regex_only(content) -> List:
    testcases1 = get_test_functions1(content)
    testcases2 = get_test_functions2(content)
    all_removed_testcases = list({*testcases1, *testcases2})
    return all_removed_testcases


#  Get list of test functions (beginning with 'test') from file changes using regex pattern
def get_test_functions1(content: str) -> List:
    removed_testcases = []
    matched_grp = re.finditer(Pattern.TEST_FUNCTION_PROTOTYPE.value, content)
    if matched_grp:
        raw_removed_testcases = [x.group() for x in matched_grp]

        for each in raw_removed_testcases:
            function_prototype = cleanup_function_prototype(each)
            function_name = get_test_function_name_from_prototype(function_prototype)
            removed_testcases.append(function_name)

        return removed_testcases
    else:
        return []


#  Get list of test functions (having annotation @Test) from file changes using regex pattern
def get_test_functions2(content: str) -> List:
    removed_testcases = []
    matched_grp = re.finditer(Pattern.TEST_FUNCTION_PROTOTYPE2.value, content)
    if matched_grp:
        raw_removed_testcases = [x.group() for x in matched_grp]

        for each in raw_removed_testcases:
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype_with_space_before(
                function_prototype
            )
            removed_testcases.append(function_name)
        return removed_testcases
    else:
        return []


TESTCASE_HISTORY_DIR = "../io/rq3/all_commits_all_testcases/"
IO_DIR = "../io/validationFiles"

projects_list = [
    #"commons-lang",
   # "gson",
  #  "commons-math",
 #   "jfreechart",
#    "joda-time",
    "pmd",
    "cts",
]

for project in projects_list:
    print("Project: ", project)

    # Test deletion commits and parents
    validation_file = "validation_diff_done_hydrated.csv"
    full_validation_file_path = Path(f"{IO_DIR}/{project}/{validation_file}")
    df = pd.read_csv(f"{full_validation_file_path}")
    deleted_test_df = df[df["Final Results"] == "yes"]
    grouped_deleted_test_df = deleted_test_df.groupby(by=["Hash", "Parent"])[
        "Removed Test Case"
    ].count()
    grouped_deleted_test_df.reset_index()
    # print(grouped_deleted_test_df)

    # Total test deletion commit
    total_test_deletion_commit = len(grouped_deleted_test_df)

    # Computer for statistics for each test deletion commit
    results = {}
    total_deleted_percent = []
    total_deleted_absolute = []
    for (hash, parent), tests_deleted in grouped_deleted_test_df.items():
        stripped_hash = strip_commit_url(hash)
        stripped_parent = strip_commit_url(parent)

        # Total deleted tests in commit
        deleted_test_in_commit = deleted_test_df[deleted_test_df["Hash"] == hash]
        total_deleted_tests_in_commit = len(deleted_test_in_commit)
        total_deleted_absolute.append(total_deleted_tests_in_commit)

        # Load test deletion commit parent file path
        testcases_file_path = (
            TESTCASE_HISTORY_DIR
            + project
            + "/"
            + project
            + "-"
            + stripped_parent
            + "-ts.txt"
        )

        # Compute total testcases present in test deletion commit parent
        total_testcases = 0
        with open(testcases_file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                testcases = compute_testcases_javaparser(line)
                if testcases is not None:
                    total_testcases += len(testcases)
                else:
                    testcases = compute_testcases_regex_only(line)
                    if testcases:
                        total_testcases += len(testcases)

        # Track total tests present and deleted at commit
        results[stripped_hash] = {
            "Total tests": total_testcases,
            "Total Deleted": total_deleted_tests_in_commit,
            "Total Deleted %": round(
                total_deleted_tests_in_commit / total_testcases * 100
            ),
        }
        total_deleted_percent.append(
            round(total_deleted_tests_in_commit / total_testcases * 100, 2)
        )

    print(results)
    print("-------------percentage------------")
    # total_deleted_percent = list(map(lambda each : each["Total Deleted %"], results))
    print("Mean: ", np.mean(total_deleted_percent))
    print("Median: ", np.median(total_deleted_percent))
    print("Q1: ", np.percentile(total_deleted_percent, 25))
    print("Q3: ", np.percentile(total_deleted_percent, 75))
    print("Max: ", np.max(total_deleted_percent))
    print("Min: ", np.min(total_deleted_percent))
    print("-------------absolute------------")
    print("Total test deletion commits: ", total_test_deletion_commit)
    print("Total deleted tests:", np.sum(total_deleted_absolute))
    print("Mean: ", np.mean(total_deleted_absolute))
    print("Median: ", np.median(total_deleted_absolute))
    print("Q1: ", np.percentile(total_deleted_absolute, 25))
    print("Q3: ", np.percentile(total_deleted_absolute, 75))
    print("Max: ", np.max(total_deleted_absolute))
    print("Min: ", np.min(total_deleted_absolute))
    print("=========================")


sys.stdout.close()
