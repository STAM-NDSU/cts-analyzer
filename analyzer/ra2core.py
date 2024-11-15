import re
from typing import List, Dict, Optional
from pydriller.domain.commit import ModifiedFile
from .utils import (
    get_function_name_from_prototype_lizard,
    get_function_name_from_prototype,
)

# import sys
# sys.stdout = open('../temp.txt', 'w')


#  Analyze commit files to detect functions removed
def analyze_functions_removal_in_commit_file(
    file: ModifiedFile,
) -> Optional[Dict[str, List]]:
    removed_functions = get_removed_functions_lizard(file)
    return removed_functions


#  Get list of removed functions from file changes [using lizard]
def get_removed_functions_lizard(file) -> List:
    methods = []
    removed_methods = []
    for x in file.methods:
        methods.append({"name": x.name, "long_name": x.long_name})
    for x in file.methods_before:
        match_found = list(filter(lambda each: each["name"] == x.name, methods))

        if not match_found:
            print("match not found")
            function_name = get_function_name_from_prototype_lizard(x.long_name)
            # Further remove parenthesis and arguments
            function_name = get_function_name_from_prototype(x.long_name)
            if function_name:
                print("funtion found", x.long_name, function_name)
                removed_methods.append(function_name)
            else:
                print(
                    "WARNING: empty function name",
                )
        else:
            function_name = get_function_name_from_prototype_lizard(x.long_name)
            function_name = get_function_name_from_prototype(x.long_name)
            # Further remove parenthesis and arguments
            print("funtion found", x.long_name, function_name)
            print("match found")
    return removed_methods


#  Get list of removed functions from file changes using javaparser
def get_removed_functions_javaparser(file) -> List:
    try:
        if not file.jp_methods_before:
            return None
    except Exception as e:
        print(e)
    print("here 3")
    methods = []
    removed_methods = []
    if file.jp_methods:
        for x in file.jp_methods:
            methods.append(x)

    if file.jp_methods_before:
        for x in file.jp_methods_before:
            match_found = list(filter(lambda each: each == x, methods))
            if not match_found:
                removed_methods.append(x)
                # print(x, "get_removed_functions_javaparser")

    return removed_methods


#  Get list of functions referenced by removed testcase from file changes using javaparser
def analyze_functions_referenced_in_removed_testcase(file, removed_test_case) -> List:
    results = file.compute_referenced_functions_in_testcase(file, removed_test_case)
    print("referenced", results)
    if results is not None:
        results = [x for x in results if not x.startswith("assert")]
        results = [x for x in results if not x == "fail"]
    return results
