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
        PROJECTS_DIR = "../io/projects"
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
fig, (ax1, ax2) = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(10, 6),
)
# # fig = plt.figure( figsize=(10,6))
# vp1 = seaborn.violinplot(
#     x="project",
#     y="commits",
#     data=new_df,
#     showfliers=False,
#     vert=True,
#     palette=color_platte,
#     split=True
#     # showmeans=True, showextrema=True, showmedians=True
# )

vp1 = ax1.violinplot(
    dataset=[
        new_df[new_df.project == "commons-lang"]["commits"].values,
        new_df[new_df.project == "commons-math"]["commits"].values,
        new_df[new_df.project == "pmd"]["commits"].values,
        new_df[new_df.project == "jfreechart"]["commits"].values,
        new_df[new_df.project == "gson"]["commits"].values,
        new_df[new_df.project == "joda-time"]["commits"].values,
    ],
    showextrema=True,
    showmeans=True,
    showmedians=True,
)


for index, pc in enumerate(vp1["bodies"]):
    pc.set_facecolor(colors[index])
    pc.set_edgecolor("black")
    pc.set_alpha(1)


vp2 = ax2.violinplot(
    dataset=[
        new_df[new_df.project == "cts"]["commits"].values,
    ],
    showextrema=True,
    showmeans=True,
    showmedians=True,
)


for pc in vp2["bodies"]:
    pc.set_facecolor(colors[-1])
    pc.set_edgecolor("black")
    pc.set_alpha(1)


# i = 0
# for pc in vp1['bodies']:
#     pc.set_facecolor(color_platte.values()[i])
#     pc.set_edgecolor('black')
#     i += 1
#     if i == len_colors:
#         i = 0
# vp1['cmeans'].set_color('black')

seaborn.set(style="darkgrid")
ax1.set_ylim(ymin=0)
# Add a vertical grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
ax1.set(
    axisbelow=True,  # Hide the grid behind plot objects
    # title='No. of deleted tests per commit',
    ylabel="Projects",
    xlabel="No. of commits",
)
fig.tight_layout()
fig.savefig("../io/rq1/figures/commits-interval-between-test-deletion-commits-violin-2.png", dpi=800)
# plt.show()


# =============