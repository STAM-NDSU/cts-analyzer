import re
import os
from datetime import datetime
from dateutil import tz
from .pattern import Pattern
from .config import Datetime_FORMAT, COMMIT_BASE_URL


# Checks if file is a candidate file
def is_candidate_test_file(filename: str) -> bool:
    if filename and re.search(Pattern.TEST_FILENAME.value, filename):
        return True
    else:
        return False


# Checks if file is a candidate file
def is_candidate_java_file(filename: str) -> bool:
    if filename and re.search(Pattern.JAVA_FILENAME.value, filename):
        return True
    else:
        return False


# Check whether directory exists or not
def check_dir_exists(directory: str) -> bool:
    return os.path.exists(directory)


# Create a new directory
def create_dir(directory: str) -> None:
    os.makedirs(directory)


# Strip characters polluting function prototype such as '+', '-', '{' and ' '
def cleanup_function_prototype(func_prototype: str) -> str:
    c = func_prototype.translate(func_prototype.maketrans("", "", "+-{")).strip()
    # c = c.replace("@Test(", "")
    # c = c.replace("@SuppressWarnings(", "")
    return c


# Strip characters polluting function name like '(', ')' and ' '
def cleanup_function_name(func_name: str) -> str:
    return func_name.translate(func_name.maketrans("", "", "()")).strip()


# Return name of function from function prototype
def get_function_name_from_prototype(function_prototype):
    func_name_search = re.search(Pattern.FUNCTION_NAME.value, function_prototype)
    func_name = ""
    if func_name_search:
        func_name = cleanup_function_name(func_name_search.group())
    return func_name


# Return name of function from function prototype [ QUICK FIX: multiple annotation issue; checks for extra space]
def get_function_name_from_prototype_with_space_before(function_prototype):
    func_name_search = re.search(
        Pattern.FUNCTION_NAME_WITH_SPACE_BEFORE.value, function_prototype
    )
    func_name = ""
    if func_name_search:
        func_name = cleanup_function_name(func_name_search.group())
    return func_name


# Return test function name from function prototype given by lizard
def get_function_name_from_prototype_lizard(function_prototype):
    return function_prototype.split("::")[-1]


# Return test function name from function prototype
def get_test_function_name_from_prototype(function_prototype):
    func_name_search = re.search(Pattern.TEST_FUNCTION_NAME.value, function_prototype)
    func_name = ""
    if func_name_search:
        func_name = cleanup_function_name(func_name_search.group())
    return func_name


# Convert datetime to local timezone
def format_commit_datetime(commit_date: datetime) -> str:
    local_datetime = commit_date.astimezone(tz.tzlocal())
    return local_datetime.strftime(Datetime_FORMAT)


# Parse commit hash as hyperlink
def parse_commit_as_hyperlink(url: str, label: str) -> str:
    return f'=HYPERLINK("{url}", "{label}")'


# Generate full url for commit hash
def get_full_commit_url(tail: str) -> str:
    return COMMIT_BASE_URL + tail


def get_full_commit_url_by_project(project: str, hash: str) -> str:
    match project:
        case "commons-lang":
            project_url = "https://github.com/apache/commons-lang/commit/"
        case "joda-time":
            project_url = "https://github.com/JodaOrg/joda-time/commit/"
        case "pmd":
            project_url = "https://github.com/pmd/pmd/commit/"
        case "gson":
            project_url = "https://github.com/google/gson/commit/"
        case "commons-math":
            project_url = "https://github.com/apache/commons-math/commit/"
        case "jfreechart":
            project_url = "https://github.com/jfree/jfreechart/commit/"
        case "cts":
            project_url = "https://android.googlesource.com/platform/cts/+/"
        case _:
            project_url = COMMIT_BASE_URL
    return project_url + hash


def parse_commit_as_hyperlink_by_project(project: str, hash: str):
    return parse_commit_as_hyperlink(
        get_full_commit_url_by_project(project, hash), hash
    )


# Parse commit hash by project
def parse_commit_hash_by_project(project: str, hash: str) -> str:
    return f'=HYPERLINK("{get_full_commit_url_by_project(project, hash)}", "{hash}")'


# Get name of repository from full url
def get_repo_name(repo_url):
    if repo_url:
        return repo_url.split("/")[-1].replace(".git", "")
    else:
        return None


# Strip commit url
def strip_commit_url(repo_url):
    if repo_url:
        return (
            repo_url.split(",")[-1].replace('"', "").replace(")", "").replace(" ", "")
        )
    else:
        return None


def strip_filepath(filepath):
    if filepath:
        return filepath.split("/")[-1]
    else:
        return None


def get_change_id_from_commit_msg(commit_msg):
    func_name_search = re.search(Pattern.CHANGE_ID.value, commit_msg)
    func_name = ""
    if func_name_search:
        return func_name_search.group()
    return func_name


def get_bug_id_from_commit_msg(commit_msg):
    func_name_search = re.search(Pattern.BUG_ID.value, commit_msg, re.IGNORECASE)
    func_name = ""
    if func_name_search:
        return func_name_search.group()
    return func_name


