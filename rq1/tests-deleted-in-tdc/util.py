"""
Generate box plot for no. of deleted tests in commit [rq1]
"""
import os.path
from pathlib import Path
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn
import numpy as np


projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

test_deletion_commits = {"project": [], "tests": []}
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("--------")
        IO_DIR = "../../io/validationFiles"
        PROJECT = project
        test_deletion_commits_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_commits.csv"
        )

        if os.path.exists(f"{test_deletion_commits_file_path}"):
            df = pd.read_csv(f"{test_deletion_commits_file_path}")

            # df = df.dropna(inplace=True)

            values = df["Total Test Cases"].values.tolist()
            
            # Compute values greater than threshold
            threshold = 100
            values_gt = [value for value in values if value > threshold ]
            print(len(values_gt))
            
            for value in values:
                if value:
                    test_deletion_commits["project"].append(project)
                    test_deletion_commits["tests"].append(value)

        print("-----*******************---")
    main(project)

df = pd.DataFrame.from_dict(test_deletion_commits)
print(df.head())
# df.to_csv('no_of_tests_deleted_in_tdc.csv', index=False)
