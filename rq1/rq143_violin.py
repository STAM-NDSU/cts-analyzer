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

OUT_DIR = "../io/rq1/figures/"

projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    "cts",
]
# Set colors
colors = ["pink", "lightblue", "lightgreen", "red", "blue", "brown", "violet"]

test_deletion_commits_range = {"project": [], "commits": []}
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        IO_DIR = "../io/validationFiles"
        PROJECT = project
        test_deletion_commits_range_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_datetime_inbetweencommits_range.csv"
        )

        if os.path.exists(f"{test_deletion_commits_range_file_path}"):
            df = pd.read_csv(f"{test_deletion_commits_range_file_path}")

            df.dropna(inplace=True)

            values = df["Commits"].values.tolist()
            for value in values:
                if value:
                    test_deletion_commits_range["project"].append(project)
                    test_deletion_commits_range["commits"].append(value)
        else:
            print("path does not exits: ", test_deletion_commits_range_file_path)

    main(project)

print(test_deletion_commits_range)
new_df = pd.DataFrame(test_deletion_commits_range, columns=["project", "commits"])
fig, ax = plt.subplots(
    figsize=(10, 6),
)
# fig = plt.figure( figsize=(10,6))
seaborn.violinplot(
    x="commits",
    y="project",
    data=new_df,
)
seaborn.set(style="whitegrid")
ax.set_xlim(xmin=0)
# Add a vertical grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax.xaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
ax.set(
    axisbelow=True,  # Hide the grid behind plot objects
    # title='No. of deleted tests per commit',
    ylabel="",
    xlabel="No. of commits",
)
fig.tight_layout()
fig.savefig("../io/rq1/figures/commits-interval-between-test-deletion-commits-violin.png", dpi=800)
# plt.show()

