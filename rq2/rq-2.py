
import sys
sys.path.append('../')

import analyzer.config as conf
from analyzer.rq2 import get_removed_testcase_and_referenced_functions_details
from analyzer.utils import *
import json
import traceback
from pathlib import Path
import pandas as pd


repo_path = conf.REPO_PATH
target_branch = conf.TARGET_BRANCH
io_dir_path = conf.OUTPUT_DIR.replace("outputRevisedLatest4", "validationFiles4")
if not repo_path:
    print("Repository path not found in .env file")
else:
    print(f"Repository Path: {repo_path}")
    try:
        # deleted tests validated file path
        full_file_path = Path(
            f"{io_dir_path}/validation_hydrated.csv"
        )
        with open(full_file_path, "r") as a:
            validated_df = pd.read_csv(f"{full_file_path}")
            validated_df = validated_df.iloc[:, 0:15]

        results_df = get_removed_testcase_and_referenced_functions_details(
            repo_path, target_branch, validated_df
        )

        if conf.HANDLE_EXPORT == "true":
            results_df.to_csv(
                f"{io_dir_path}/hydrated_rq_2.csv",
                index=False,
            )

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        # print(e)
        traceback.print_exc()
