import analyzer.config as conf
from analyzer.helpers import export_to_csv
from analyzer.analyzer import get_removed_test_functions_and_assertions_details
from analyzer.utils import *
from analyzer.config import OUTPUT_DIRECTORY, OUTPUT_FILENAME
import json
import pydriller

refactoring_file = open(conf.REFACTOR_FILE)
refactorings_data = json.load(refactoring_file)["commits"]

repo_path = conf.REPO_PATH
target_branch = conf.TARGET_BRANCH
if repo_path:
    print(f"Repository Path: {repo_path}")
    try:
        results = get_removed_test_functions_and_assertions_details(repo_path, target_branch, refactorings_data)
        if conf.HANDLE_EXPORT == "true":
            export_to_csv(headers=conf.CSV_HEADERS, records=results, dir=OUTPUT_DIRECTORY, filename=OUTPUT_FILENAME)
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        print(e)
else:
    print("Repository path not found in .env file")

refactoring_file.close()
