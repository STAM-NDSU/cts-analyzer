import re
from typing import List, Collection, Tuple
from pydriller.domain.commit import ModifiedFile
from .utils import cleanup_function_prototype, get_function_name_from_prototype, get_test_function_name_from_prototype
from .pattern import Pattern
from . import config


#  Analyze commit files to detect tests cases(functions and assertions) removed
def analyze_test_cases_removal_in_commit_file(file: ModifiedFile, all_added_test_cases_in_commit: List) -> Collection[Tuple[str, bool]]:
    file_changes = file.diff  
    candidate_removed_test_functions = get_removed_test_functions(file_changes, file)
    candidate_added_test_functions = get_added_test_functions(file_changes, file)
    refactored_test_functions = get_refactored_test_functions(file_changes, file)
    removed_test_functions = []

    print(file.testcases)
    print("_____")
    print(file.testcases_before)
    # Added test functions across modified files in a commit
    all_added_test_cases_in_commit += candidate_added_test_functions

    for candidate_removed_test_function in candidate_removed_test_functions:
        if config.HANDLE_MOVED == "true":
            # Check if the removed test function is refactored test case i.e. false positive
            if candidate_removed_test_function in refactored_test_functions:
                continue

            # Check if test function is moved to different file in same commit
            # becomes removed from one file and added in another file; false positive
            if candidate_removed_test_function in all_added_test_cases_in_commit:
                continue
            # print(candidate_removed_test_function, "candidate")
        removed_test_functions.append(candidate_removed_test_function)
    # print(len(removed_test_functions), "total candidate")
    result = {}
    # Deleted tests in a modified file having no added tests is of HIGH confidence
    if len(candidate_added_test_functions) == 0:
        result["removed_test_functions"] = removed_test_functions
        result['confidence'] = "HIGH"
    else:
        result["removed_test_functions"] = removed_test_functions
        result['confidence'] = "LOW"

    return result


#  Get list of removed test functions from file changes
def get_removed_test_functions(file_changes: str, file) -> List:
    removed_testcases = []
    matched_grp = re.finditer(Pattern.REMOVED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    
    if matched_grp:
        raw_removed_testcases = [x.group() for x in matched_grp]
        
        for each in raw_removed_testcases:
            # print(each, file.filename, "removed")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            print(function_name, file.filename, "removed")
            removed_testcases.append(function_name)
        
        removed_testcases2 = get_removed_test_functions2(file_changes, file)
        all_removed_testcases_before_lizard = list({*removed_testcases, *removed_testcases2})
        removed_testcases_lizard = get_removed_test_functions_lizard(file_changes, file, all_removed_testcases_before_lizard)
        all_removed_testcases = list({*all_removed_testcases_before_lizard, *removed_testcases_lizard})
        print(all_removed_testcases, "all removed")
        return all_removed_testcases
    else:
        return  []


#  Get list of removed test functions from file changes using lizard
def get_removed_test_functions_lizard(file_changes: str, file, all_removed_testcases_before_lizard) -> List:
    methods = []
    removed_methods = []
    for x in file.methods:
        methods.append({"name": x.name, "long_name": x.long_name})
    for x in file.methods_before:
        match_found = list(filter(lambda each: each["name"] == x.name, methods))
        if not match_found:
            function_name = get_test_function_name_from_prototype(x.long_name)
            if function_name and function_name not in all_removed_testcases_before_lizard:
                # print(function_name, "removed lizard")
                removed_methods.append(function_name)

    return removed_methods
    
#  Get list of removed test functions from file changes
def get_removed_test_functions2(file_changes: str, file) -> List:
    removed_testcases = []
    matched_grp = re.finditer(Pattern.REMOVED_TEST_FUNCTION_PROTOTYPE2.value, file_changes)
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


#  Get refactored test functions from file changes
def get_refactored_test_functions(file_changes: str, file) -> List:
    refactored_testcases = []
    matched_grp = re.finditer(Pattern.REFACTORED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    if matched_grp:
        raw_refactored_testcases = [x.group() for x in matched_grp]
        
        for each in raw_refactored_testcases:
            # print(each, file.filename, "refactored")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            refactored_testcases.append(function_name)
            # print(function_name, file.filename, "refactored")
        
        refactored_testcases2 = get_refactored_test_functions2(file_changes, file)
        
        return list({*refactored_testcases2, *refactored_testcases})
    else:
        return []

#  Get list of refactored test functions from file changes
def get_refactored_test_functions2(file_changes: str, file) -> List:
    refactored_testcases = []
    matched_grp = re.finditer(Pattern.REFACTORED_TEST_FUNCTION_PROTOTYPE2.value, file_changes)
    if matched_grp:
        raw_refactored_testcases = [x.group() for x in matched_grp]

        for each in raw_refactored_testcases:
            # print(each, file.filename, "refactored 2")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            refactored_testcases.append(function_name)
            # print(function_name, file.filename, "refactored 2")

        return refactored_testcases
    else:
        return []
    
#  Get added test functions from file changes
def get_added_test_functions(file_changes: str, file) -> List:
    added_testcases = []
    matched_grp = re.finditer(Pattern.ADDED_TEST_FUNCTION_PROTOTYPE.value, file_changes)
    if matched_grp:
        
        raw_added_testcases = [x.group() for x in matched_grp]
        
        for each in raw_added_testcases:
            # print(each, file.filename, "added")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            added_testcases.append(function_name)
            # print(function_name, file.filename, "added")
            
        added_testcases2 = get_added_test_functions2(file_changes, file)
        all_added_testcases_before_lizard = list({*added_testcases, *added_testcases2})
        added_testcases_lizard = get_added_test_functions_lizard(file_changes, file, all_added_testcases_before_lizard)
        all_added_testcases = list({*all_added_testcases_before_lizard, *added_testcases_lizard})
        print(all_added_testcases, "all added")
        return all_added_testcases
    else:
        return []


def get_added_test_functions_lizard(file_changes: str, file, all_added_testcases_before_lizard) -> List:
    methods_before = []
    added_methods = []
    for x in file.methods_before:
        methods_before.append({"name": x.name, "long_name": x.long_name})
    for x in file.methods:
        match_found = list(filter(lambda each: each["name"] == x.name, methods_before))
        if not match_found:
            function_name = get_test_function_name_from_prototype(x.long_name)
            if function_name and function_name not in all_added_testcases_before_lizard:
                # print(function_name, "added lizard")
                added_methods.append(function_name)

    return added_methods

#  Get added test functions from file changes
def get_added_test_functions2(file_changes: str, file) -> List:
    added_testcases = []
    matched_grp = re.finditer(Pattern.ADDED_TEST_FUNCTION_PROTOTYPE2.value, file_changes)
    if matched_grp:
        
        raw_added_testcases = [x.group() for x in matched_grp]
       
        for each in raw_added_testcases:
            # print(each, file.filename, "added2")
            function_prototype = cleanup_function_prototype(each)
            function_name = get_function_name_from_prototype(function_prototype)
            added_testcases.append(function_name)
            # print(function_name, file.filename, "added2")
        return added_testcases
    else:
        return []
    
#  Get removed test assertions from file changes
def get_removed_test_assertions(file_changes: str, file) -> List:
    removed_assertions = []
    matched_grp = re.finditer(Pattern.REMOVED_ASSERT_FUNCTION_PROTOTYPE.value, file_changes)
    if matched_grp:
        raw_removed_assertions = [x.group() for x in matched_grp]

        for each in raw_removed_assertions:
            function_prototype = cleanup_function_prototype(each)
            removed_assertions.append(function_prototype)

        return removed_assertions
    else:
        return []



