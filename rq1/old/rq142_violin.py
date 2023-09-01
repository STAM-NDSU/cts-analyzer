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
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]
medians = []
test_deletion_commits_timerange = {"project": [], "days": []}
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        IO_DIR = "../io/validationFiles"
        PROJECTS_DIR = "./../os-java-projects"
        PROJECT = project
        test_deletion_commits_timerange_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_datetime_inbetweencommits_range.csv"
        )

        if os.path.exists(f"{test_deletion_commits_timerange_file_path}"):
            df = pd.read_csv(f"{test_deletion_commits_timerange_file_path}")

            df.dropna(inplace=True)

            values = df["Range"].values.tolist()
            for value in values:
                if value:
                    test_deletion_commits_timerange["project"].append(project)
                    test_deletion_commits_timerange["days"].append(value)
        else:
            print("path does not exits: ", test_deletion_commits_timerange_file_path)

    main(project)

print(test_deletion_commits_timerange)
new_df = pd.DataFrame(test_deletion_commits_timerange, columns=["project", "days"])
fig, ax = plt.subplots(
    figsize=(10, 6),
)
# fig = plt.figure( figsize=(10,6))
seaborn.violinplot(
    x="days",
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
    xlabel="No. of days",
)
fig.tight_layout()
fig.savefig(
    "../io/rq1/figures/time-interval-between-test-deletion-commits-violin.png", dpi=800
)
# plt.show()
