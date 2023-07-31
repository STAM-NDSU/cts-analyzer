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
import seaborn
import numpy as np
OUT_DIR = 'io/rq1/figures/'
# plt.rcParams["figure.figsize"] = [4,3]
# plt.rcParams["figure.autolayout"] = True
projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    # "cts",
]
medians = []
test_deletion_commits = {"project": [], "deleted tests in commit": []}
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        IO_DIR = "io/validationFiles"
        PROJECTS_DIR = "io/projects"
        PROJECT = project
        test_deletion_commits_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_commits.csv"
        )

        if os.path.exists(f"{test_deletion_commits_file_path}"):
            df = pd.read_csv(f"{test_deletion_commits_file_path}")
           
            # df = df.dropna(inplace=True)
           
            values = df["Total Test Cases"].values.tolist()
            print(values)
            for value in values:
                if value:
                    test_deletion_commits["project"].append(project)
                    test_deletion_commits["deleted tests in commit"].append(value)

    main(project)



new_df = pd.DataFrame(test_deletion_commits, columns=['project', 'deleted tests in commit'])
fig = plt.figure( figsize=(10,6))
seaborn.violinplot(x="project", y="deleted tests in commit", data=new_df,  showfliers=False, xlabel="da", vert=True, )
plt.show()
# seaborn.set(style='whitegrid')
# # tip = seaborn.load_dataset('tips')
 
# seaborn.boxplot(x='h', y='h', data=list(test_deletion_commits.values()))
# plt.show()
# # test_deletion_commits_df = pd.DataFrame(test_deletion_commits)
# # print(test_deletion_commits_df)

# ===================
# # Generate box plot for total tests deleted
# # fig = plt.figure()
# # ax = fig.add_axes([0, 0, 1, 1])
# fig, ax = plt.subplots(
#     figsize=(5,3),
# )
# bp = ax.boxplot(
#     list(test_deletion_commits.values()),
#     showfliers=False,
#     # notch=True,  # notch shape
#     vert=False,  # vertical box alignment
#     patch_artist=True,  # fill with color
#     #  labels=[]  # will be used to label x-ticks
# )

# # Set boxes, whiskers and fliers config
# plt.setp(bp["boxes"], color="black")
# plt.setp(bp["whiskers"], color="black")
# # plt.setp(bp['fliers'], color='red', marker='+')

# # Set colors
# colors = [
#     "pink",
#     "lightblue",
#     "lightgreen",
#     "red",
#     "blue",
#     "brown",
#     # 'violet'
# ]
# for patch, color in zip(bp["boxes"], colors):
#     patch.set_facecolor(color)

# # Add a vertical grid to the plot, but make it very light in color
# # so we can use it for reading data values but not be distracting
# ax.xaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)

# ax.set(
#     axisbelow=True,  # Hide the grid behind plot objects
#     # title='No. of deleted tests per commit',
#     # ylabel="Projects",
#     xlabel="No. of tests deleted",
# )

# # # Set the axes ranges and axes labels
# # ax.set_xlim(0.5, 100)
# # top = 40
# # bottom = -5
# # ax.set_ylim(bottom, top)
# ax.set_yticklabels(list(test_deletion_commits.keys()))


# # Due to the Y-axis scale being different across samples, it can be
# # hard to compare differences in medians across the samples. Add upper
# # X-axis tick labels with the sample medians to aid in comparison
# # (just use two decimal places of precision)
# # pos = np.arange(7) + 1
# # upper_labels = [str(round(s, 2)) for s in medians]
# # weights = ["bold", "semibold"]
# # for tick, label in zip(range(7), ax.get_yticklabels()):
# #     k = tick % 2
# #     ax.text(
# #         pos[tick],
# #         0.97,
# #         upper_labels[tick],
# #         transform=ax.get_yaxis_transform(),
# #         horizontalalignment="center",
# #         size="x-small",
# #         #  weight=weights[k], color=box_colors[k]
# #     )
# fig.tight_layout()
# fig.savefig(OUT_DIR = 'io/rq1/figures/' + "no-of-deleted-tests.png",
#             dpi=800)
# # plt.show()
