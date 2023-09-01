import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load env variables
load_dotenv()

# Url to cts repo
REPO_PATH = os.getenv("REPO_PATH", None)

# Branch of the cts repo to be analyzed
TARGET_BRANCH = os.getenv("TARGET_BRANCH", "master")

# Url to cts repo
COMMIT_BASE_URL = os.getenv(
    "COMMIT_BASE_URL", "https://android.googlesource.com/platform/cts/+/"
)

# Directory where generated csv file is stored
HANDLE_EXPORT = os.getenv("HANDLE_EXPORT", "false")
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIR", "../output")

# Refactors file generated from Refactoring Minor(https://github.com/tsantalis/RefactoringMiner)
# used to filter out false positive
REFACTOR_FILE = "./io/files/" + os.getenv("REFACTOR_FILE", "refactorings.json")
HANDLE_REFACTOR = os.getenv("HANDLE_REFACTOR", "false")
HANDLE_MOVED = os.getenv("HANDLE_MOVED", "false")

# Valid java file extensions
JAVA_FILE_EXT = [".java"]

# Generated csv file headers
CSV_HEADERS = [
    "Datetime",
    "Hash",
    "Parent",
    "Author",
    "Commit Msg",
    "Filepath",
    "Filename",
    "Removed Test Case",
]

DEFAULT_COMMIT_RANGE_DAYS_INTERVAL = 365

# Datetime formats
DATE_FORMAT = "%m/%d/%Y"
Datetime_FORMAT = "%m/%d/%Y %H:%M:%S"

# Commit daterange filters
COMMIT_START_DATE = os.getenv("COMMIT_START_DATE")
COMMIT_END_DATE = os.getenv("COMMIT_END_DATE")
now = datetime.now()
# Define interval in no of days to compute relative time diff
interval = int(os.getenv("CTS_COMMIT_INTERVAL", DEFAULT_COMMIT_RANGE_DAYS_INTERVAL))
COMMIT_START_DATETIME = (
    datetime.strptime(COMMIT_START_DATE, DATE_FORMAT)
    if COMMIT_START_DATE
    else (now - timedelta(days=interval))
)
COMMIT_END_DATETIME = (
    datetime.strptime(COMMIT_END_DATE, DATE_FORMAT) if COMMIT_START_DATE else now
)


OUTPUT_DIR = os.getenv("OUTPUT_DIR", "io/cts")

# Filename of generated csv file
PROJECT = os.getenv("PROJECT", "cts")
STEP = os.getenv("STEP", "step-1")
# date_format = "%m-%d-%Y"
# parsed_COMMIT_START_DATE = COMMIT_START_DATETIME.strftime(date_format)
# parsed_COMMIT_END_DATE = COMMIT_END_DATETIME.strftime(date_format)
# OUTPUT_FILENAME = BASE_FILENAME + '.csv'
BASE_FILENAME = PROJECT + "-" + STEP
OUTPUT_FILENAME = BASE_FILENAME + ".csv"
