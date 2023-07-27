"""
Generate box plot for no. of deleted tests in commit [rq1]
"""
import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import strip_commit_url
from datetime import datetime
import os
import json
import matplotlib.pyplot as plt
import numpy as np

# plt.rcParams["figure.figsize"] = [4,3]
# plt.rcParams["figure.autolayout"] = True
# Set colors
colors = [
    "pink",
    "lightblue",
    "lightgreen",
    "red",
    "blue",
    "brown",
    # 'violet'
]
projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    # "cts",
]

fig, ax = plt.subplots(
    figsize=(10, 6),
)
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        IO_DIR = "io/validationFiles"
        PROJECT = project
        stat_test_deletion_commits_grouped_year_file_path = Path(
            f"{IO_DIR}/{PROJECT}/stat_test_deletion_commits_grouped_year.csv"
        )

        if os.path.exists(f"{stat_test_deletion_commits_grouped_year_file_path}"):
            df = pd.read_csv(f"{stat_test_deletion_commits_grouped_year_file_path}")
            ax.plot(df["Datetime"].values.tolist(), df["Testcase"].values.tolist(), color=colors[index] )

    main(project)


plt.xlabel("Year")
plt.ylabel("No. of tests deleted")
fig.savefig("tests-deleted-per-year.png", dpi=800)
# plt.show()
