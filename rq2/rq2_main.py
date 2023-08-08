import sys

sys.path.append("../")

import analyzer.config as conf
from analyzer.rq2 import get_removed_testcase_and_referenced_functions_details
from analyzer.utils import *
import json
import traceback
from pathlib import Path
import pandas as pd


projects = [
    # {
    #     "project": "commons-lang",
    #     "branch": "master",
    # },
    # {
    #     "project": "gson",
    #     "branch": "master",
    # },
    # {
    #     "project": "commons-math",
    #     "branch": "master",
    # },
    # {
    #     "project": "joda-time",
    #     "branch": "main",
    # },
    {
        "project": "pmd",
        "branch": "master",
    },
    # {
    #     "project": "jfreechart",
    #     "branch": "master",
    # },
    # {
    #     "project": "cts",
    #     "branch": "master",
    # },
]

for project_info in projects:
    project, target_branch = project_info["project"], project_info["branch"]
    repo_path = "../io/projects/" + project
    validation_dir = "../io/validationFiles/" + project

    if not repo_path:
        print("Repository path not found in .env file")
    else:
        print(f"Repository Path: {repo_path}")
        try:
            # deleted tests validated file path
            full_file_path = Path(f"{validation_dir}/validation_diff_done_hydrated.csv")
            with open(full_file_path, "r") as a:
                df = pd.read_csv(f"{full_file_path}")
                test_deletion_df = df[df["Final Results"] == "yes"]

                print(project, test_deletion_df.shape[0])
                print("Total commits",  len(list(test_deletion_df["Hash"].dropna().unique())))

            # results_df = get_removed_testcase_and_referenced_functions_details(
            #     project, repo_path, target_branch, test_deletion_df
            # )

            # print("results_df", results_df.shape[0])
            # if conf.HANDLE_EXPORT == "true":
            #     results_df.to_csv(
            #         f"{validation_dir}/hydrated_rq_2.csv",
            #         index=False,
            #     )
            #     print(f'Successfully generated {validation_dir}/hydrated_rq_2.csv')

        except Exception as e:
            print(f"Error occurred: {type(e).__name__}")
            # print(e)
            traceback.print_exc()
