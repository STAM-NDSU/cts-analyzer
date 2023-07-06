import os
import javalang
from typing import Optional, List
from analyzer.utils import (
    is_candidate_file,
)
from analyzer.pattern import Pattern
import re
from analyzer.utils import (
    cleanup_function_prototype,
    get_function_name_from_prototype_with_space_before,
    get_test_function_name_from_prototype,
)

import sys
# Redirect console ouput to a file
sys.stdout = open('./stats/all_repos_testcases_stat.txt', 'w')

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


target_dir = "./io/projects/"
projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

for each in projects_list:
    print("Project: ", each)
    repo_path = target_dir + each
    print(repo_path)
    files_not_parsed = []
    total_files_not_parsed=0
    total_test_files = 0
    total_parsed_test_cases = 0
    total_regex_test_cases = 0

    for root, dirs, files in os.walk(repo_path, topdown=False):
        for name in files:
            if is_candidate_file(name):
                total_test_files += 1

                with open(os.path.join(root, name), "r") as f:
                    content = f.read()
                    testcases = compute_testcases_javaparser(content)
                    if testcases is not None:
                        total_parsed_test_cases += len(testcases)
                    else:
                        total_files_not_parsed += 1
                        files_not_parsed.append(os.path.join(root, name))
                        testcases = compute_testcases_regex_only(content)
                        if testcases:
                            total_regex_test_cases += len(testcases)

    print("Total Test Files: ", total_test_files)
    print("Total Test Files Parsed:: ", total_test_files - total_files_not_parsed)
    print("Total Test Files Not Parsed:: ", total_files_not_parsed)
    for each in files_not_parsed:
        print(each)
    print("Total Parsed Testcases: ", total_parsed_test_cases)
    print("Total Regex Testcases: ", total_regex_test_cases)
    print("Total Testcases: ", total_regex_test_cases + total_parsed_test_cases)
    print("=========================")

    # Handle for directories
    # for name in dirs:
    #     print(os.path.join(root, name))
    


sys.stdout.close()