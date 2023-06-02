import re
from typing import List, Collection, Tuple
from pydriller.domain.commit import ModifiedFile
from .utils import (
    cleanup_function_prototype,
    get_function_name_from_prototype,
    get_test_function_name_from_prototype,
    get_function_name_from_prototype_lizard,
)
from .pattern import Pattern
from . import config


#  Analyze commit files to detect tests cases removed
def analyze_test_cases_removal_in_commit_file(
    file: ModifiedFile,
) -> Collection[Tuple[str, bool]]:
    removed_test_functions = get_removed_test_functions(file)
    result = {"removed_test_functions": removed_test_functions}
    return result


#   # Added test functions across modified files in a commit
def analyze_test_cases_addition_in_commit_file(
    file: ModifiedFile, all_added_test_cases_in_commit: List
) -> List:
    added_test_functions = get_added_test_functions(file)
    all_added_test_cases_in_commit += added_test_functions
    return all_added_test_cases_in_commit


def analyze_true_test_cases_deletion_in_commit_file(
    file: ModifiedFile, all_false_removed_test_cases_in_file: List
) -> List:
    true_removed_test_functions_javaparser = get_true_removed_test_functions_javaparser(
        file
    )
    all_false_removed_test_cases_in_file += true_removed_test_functions_javaparser
    return all_false_removed_test_cases_in_file


#  Get list of removed test functions from file changes
def get_removed_test_functions(file) -> List:
    # removed_testcases = []
    # matched_grp = re.finditer(Pattern.REMOVED_TEST_FUNCTION_PROTOTYPE.value, file_changes)

    # if matched_grp:
    #     raw_removed_testcases = [x.group() for x in matched_grp]

    #     for each in raw_removed_testcases:
    #         # print(each, file.filename, "removed")
    #         function_prototype = cleanup_function_prototype(each)
    #         function_name = get_function_name_from_prototype(function_prototype)
    #         print(function_name, file.filename, "removed")
    #         removed_testcases.append(function_name)

    #     removed_testcases2 = get_removed_test_functions2(file_changes, file)
    #     all_removed_testcases_before_lizard = list({*removed_testcases, *removed_testcases2})
    #     removed_testcases_lizard = get_removed_test_functions_lizard(file_changes, file, all_removed_testcases_before_lizard)
    #     all_removed_testcases = list({*all_removed_testcases_before_lizard, *removed_testcases_lizard})
    #     print(all_removed_testcases, "all removed")
    #     return all_removed_testcases
    removed_testcases_lizard = get_removed_test_functions_lizard(file)
    return removed_testcases_lizard
    # else:
    #     return  []


def get_removed_test_functions_regex_only(file) -> List:
    removed_testcases1 = get_removed_test_functions1(file.diff)
    removed_testcases2 = get_removed_test_functions2(file.diff)
    all_removed_testcases = list({*removed_testcases1, *removed_testcases2})
    return all_removed_testcases


#  Get list of removed test functions from file changes
def get_removed_test_functions1(file_changes: str) -> List:
    removed_testcases = []
    matched_grp = re.finditer(
        Pattern.REMOVED_TEST_FUNCTION_PROTOTYPE.value, file_changes
    )
    if matched_grp:
        raw_removed_testcases = [x.group() for x in matched_grp]

        for each in raw_removed_testcases:
            # print(each, file.filename, "removed 2")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            removed_testcases.append(function_name)
            # print(function_name, file.filename, "removed 2")

        return removed_testcases
    else:
        return []


#  Get list of removed test functions from file changes
def get_removed_test_functions2(file_changes: str) -> List:
    removed_testcases = []
    matched_grp = re.finditer(
        Pattern.REMOVED_TEST_FUNCTION_PROTOTYPE2.value, file_changes
    )
    if matched_grp:
        raw_removed_testcases = [x.group() for x in matched_grp]

        for each in raw_removed_testcases:
            # print(each, file.filename, "removed 2")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            removed_testcases.append(function_name)
            # print(function_name, file.filename, "removed 2")

        return removed_testcases
    else:
        return []


#  Get list of removed test functions from file changes using lizard
def get_removed_test_functions_lizard(file) -> List:
    methods = []
    removed_methods = []
    for x in file.methods:
        methods.append({"name": x.name, "long_name": x.long_name})
    for x in file.methods_before:
        match_found = list(filter(lambda each: each["name"] == x.name, methods))
        if not match_found:
            function_name = get_test_function_name_from_prototype(x.long_name)
            if function_name:
                print(function_name, "removed lizard", "check_annot no")
                removed_methods.append({"name": function_name, "check_annot": "no"})
            else:
                function_name = get_function_name_from_prototype(x.long_name)
                print(function_name, "removed lizard", "check_annot")
                removed_methods.append({"name": function_name, "check_annot": "check"})
    return removed_methods


# #  Get refactored test functions from file changes
# def get_refactored_test_functions(file_changes: str, file) -> List:
#     refactored_testcases = []
#     matched_grp = re.finditer(Pattern.REFACTORED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
#     if matched_grp:
#         raw_refactored_testcases = [x.group() for x in matched_grp]

#         for each in raw_refactored_testcases:
#             # print(each, file.filename, "refactored")
#             function_prototype = cleanup_function_prototype(each)
#             function_name = get_function_name_from_prototype(function_prototype)
#             refactored_testcases.append(function_name)
#             # print(function_name, file.filename, "refactored")

#         refactored_testcases2 = get_refactored_test_functions2(file_changes, file)

#         return list({*refactored_testcases2, *refactored_testcases})
#     else:
#         return []

# #  Get list of refactored test functions from file changes
# def get_refactored_test_functions2(file_changes: str, file) -> List:
#     refactored_testcases = []
#     matched_grp = re.finditer(Pattern.REFACTORED_TEST_FUNCTION_PROTOTYPE2.value, file_changes)
#     if matched_grp:
#         raw_refactored_testcases = [x.group() for x in matched_grp]

#         for each in raw_refactored_testcases:
#             # print(each, file.filename, "refactored 2")
#             function_prototype = cleanup_function_prototype(each)
#             function_name = get_function_name_from_prototype(function_prototype)
#             refactored_testcases.append(function_name)
#             # print(function_name, file.filename, "refactored 2")

#         return refactored_testcases
#     else:
#         return []


#  Get added test functions from file changes
def get_added_test_functions(file) -> List:
    # added_testcases = []
    # matched_grp = re.finditer(Pattern.ADDED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    # if matched_grp:

    #     raw_added_testcases = [x.group() for x in matched_grp]

    #     for each in raw_added_testcases:
    #         # print(each, file.filename, "added")
    #         function_prototype = cleanup_function_prototype(each)
    #         function_name = get_function_name_from_prototype(function_prototype)
    #         added_testcases.append(function_name)
    #         # print(function_name, file.filename, "added")

    #     added_testcases2 = get_added_test_functions2(file_changes, file)
    #     all_added_testcases_before_lizard = list({*added_testcases, *added_testcases2})
    #     added_testcases_lizard = get_added_test_functions_lizard(file_changes, file, all_added_testcases_before_lizard)
    #     all_added_testcases = list({*all_added_testcases_before_lizard, *added_testcases_lizard})
    #     print(all_added_testcases, "all added")
    #     return all_added_testcases
    added_testcases_lizard = get_added_test_functions_lizard(file)
    return added_testcases_lizard
    # else:
    #     return []


def get_added_test_functions_lizard(file) -> List:
    methods_before = []
    added_methods = []
    for x in file.methods_before:
        methods_before.append({"name": x.name, "long_name": x.long_name})
    for x in file.methods:
        match_found = list(filter(lambda each: each["name"] == x.name, methods_before))
        if not match_found:
            function_name = get_function_name_from_prototype(x.long_name)
            if function_name:
                added_methods.append(function_name)
    return added_methods


#  Get false removed test functions from file changes
def get_true_removed_test_functions_javaparser(file) -> List:
    true_removed_test_functions_javaparser = get_true_removed_test_functions_javaparser(
        file
    )
    return true_removed_test_functions_javaparser


#  Get list of removed test functions from file changes using lizard
def get_true_removed_test_functions_javaparser(file) -> List:
    methods = []
    removed_methods = []
    if file.testcases:
        for x in file.testcases:
            methods.append(x)
    if file.testcases_before:
        for x in file.testcases_before:
            match_found = list(filter(lambda each: each == x, methods))
            if not match_found:
                removed_methods.append(x)
    return removed_methods


# #  Get added test functions from file changes
# def get_added_test_functions2(file_changes: str, file) -> List:
#     added_testcases = []
#     matched_grp = re.finditer(Pattern.ADDED_TEST_FUNCTION_PROTOTYPE2.value, file_changes)
#     if matched_grp:

#         raw_added_testcases = [x.group() for x in matched_grp]

#         for each in raw_added_testcases:
#             # print(each, file.filename, "added2")
#             function_prototype = cleanup_function_prototype(each)
#             function_name = get_function_name_from_prototype(function_prototype)
#             added_testcases.append(function_name)
#             # print(function_name, file.filename, "added2")
#         return added_testcases
#     else:
#         return []
