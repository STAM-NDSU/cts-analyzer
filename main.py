import analyzer.config as conf
from analyzer.helpers import export_to_csv
from analyzer.analyzer import get_removed_test_functions_details
from analyzer.utils import *
from analyzer.config import OUTPUT_DIRECTORY, OUTPUT_FILENAME
import json
import traceback
from pathlib import Path
import pandas as pd


repo_path = conf.REPO_PATH
target_branch = conf.TARGET_BRANCH
if not repo_path:
    print("Repository path not found in .env file")
else:
    print(f"Repository Path: {repo_path}")
    try:
        # Get candidate test deletion commits
        if conf.STEP == "step1":
            results = get_removed_test_functions_details(
                repo_path, target_branch, 1, None
            )
            
            if conf.HANDLE_EXPORT == "true":
                headers = conf.CSV_HEADERS
                export_to_csv(
                    headers=conf.CSV_HEADERS,
                    records=results,
                    dir=OUTPUT_DIRECTORY,
                    filename="hydrated_" + OUTPUT_FILENAME,
                )
        # Get candidate deleted tests and refine candidate test deletion commits
        elif conf.STEP == "step2":
            print("Start step 2-------")
            full_file_path = Path(
                f"{conf.OUTPUT_DIR}/hydrated_{conf.PROJECT}-step1.csv"
            )
            full_refined_file_path = Path(
                f"{conf.OUTPUT_DIR}/hydrated_{conf.PROJECT}-step1_refined.csv"
            )

            # Check if step 1 file is refined for the project [Use refined file if available]
            if os.path.exists(f"{full_refined_file_path}"):
                full_file_path = full_refined_file_path

            with open(full_file_path, "r") as a:
                step1_hydrated_df = pd.read_csv(f"{full_file_path}")
                step2_df = get_removed_test_functions_details(
                    repo_path, target_branch, 2, step1_hydrated_df
                )

                if conf.HANDLE_EXPORT == "true":
                    step2_df.to_csv(
                        f"{conf.OUTPUT_DIR}/hydrated_{conf.PROJECT}-step2.csv",
                        index=False,
                    )
                    print(
                        f"Successfully generated {conf.OUTPUT_DIR}/hydrated_{conf.PROJECT}-step2.csv"
                    )
                print("------- END step 2")

        # Filter our refactored test cases [ suggested by RefMiner]
        elif conf.STEP == "step3":
            print("Start step 3-------")
            refactoring_file = open(conf.REFACTOR_FILE)
            refactorings_data = json.load(refactoring_file)["commits"]

            full_file_path = Path(
                f"{conf.OUTPUT_DIR}/hydrated_{conf.PROJECT}-step2.csv"
            )
            with open(full_file_path, "r") as a:
                df = pd.read_csv(f"{full_file_path}")
                # df = df.iloc[:, 0:7]
                new_df = pd.DataFrame()

                for index, row in df.iterrows():
                    is_refactor = False
                    testcase_filename = row["Filename"]
                    testcase_hash = strip_commit_url(row["Hash"])
                    testcase_name = str(
                        row["Removed Test Case"]
                    )  # TO FIX: gson issue "string as left operand, not float in 'in each["codeElement"]'"
                    testcase_filepath = row["Filepath"]
                    # print(testcase_hash, testcase_name, testcase_filepath)

                    # refactors_commit_data = list(filter(lambda each: each["sha1"] == commit.hash, repo_refactors))[0]
                    refactors_commit_data = next(
                        (
                            each
                            for each in refactorings_data
                            if each["sha1"] == testcase_hash
                        ),
                        None,
                    )

                    refactors_commit = (
                        refactors_commit_data["refactorings"]
                        if not refactors_commit_data is None
                        else []
                    )

                    # Check if testcase is refactored [e.g Rename Method - method is refactored]
                    for refactor in refactors_commit:
                        for each in refactor["leftSideLocations"]:
                            if (
                                each["codeElement"]
                                and (testcase_name in each["codeElement"])
                                and (testcase_filepath == each["filePath"])
                            ):
                                is_refactor = True
                                break

                    # Check if test class is renamed [e.g Rename Class- all methods are refactored]
                    if not is_refactor:
                        for refactor in refactors_commit:
                            if refactor["type"] == "Rename Class":
                                for each in refactor["leftSideLocations"]:
                                    if each["codeElement"] and (
                                        testcase_filepath == each["filePath"]
                                    ):
                                        is_refactor = True
                                        break

                    # Append only not refactored testcase
                    if not is_refactor:
                        new_df = pd.concat([new_df, pd.DataFrame([row])], ignore_index=True)
                        # new_df.loc[len(new_df)] = row
                        # new_df = new_df.append(row, ignore_index=True) # old before pandas v2.0

                if conf.HANDLE_EXPORT == "true":
                    new_df.to_csv(
                        f"{conf.OUTPUT_DIR}/hydrated_{conf.OUTPUT_FILENAME}",
                        index=False,
                    )
                    print(
                        f"Successfully generated {conf.OUTPUT_DIR}/hydrated_{conf.OUTPUT_FILENAME}"
                    )

            refactoring_file.close()
            print("------- End step 3")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        # print(e)
        traceback.print_exc()
