"""
Generate box plot for no. of commits between consequtive test deletion commits [rq1]
"""
import os.path
from pathlib import Path
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = "../../io/rq1/figures/"

# plt.rcParams["figure.figsize"] = [4,3]
# plt.rcParams["figure.autolayout"] = True
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
test_deletion_commits_range = {}
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        IO_DIR = "../../io/validationFiles"
        PROJECTS_DIR = "./../../os-java-projects"
        PROJECT = project
        test_deletion_datetime_inbetweencommits_range_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_datetime_inbetweencommits_range.csv"
        )

        if os.path.exists(f"{test_deletion_datetime_inbetweencommits_range_file_path}"):
            df = pd.read_csv(
                f"{test_deletion_datetime_inbetweencommits_range_file_path}"
            )
            df.dropna(inplace=True)
            test_deletion_commits_range[project] = df["Commits"].values.tolist()
            medians.append(np.median(test_deletion_commits_range[project]))

    main(project)

# test_deletion_commits_df = pd.DataFrame(test_deletion_commits)
# print(test_deletion_commits_df)

# Generate box plot for total tests deleted
# fig = plt.figure()
# ax = fig.add_axes([0, 0, 1, 1])


fig, (ax1, ax2) = plt.subplots(
    1,
    2,
    figsize=(5, 3),
    # sharey=True
)
# # Share a X axis with each column of subplots
# plt.subplots(2, 2, sharex='col')


bp1 = ax1.boxplot(
    list(test_deletion_commits_range.values())[:6],
    showfliers=False,
    # notch=True,  # notch shape
    vert=False,  # vertical box alignment
    patch_artist=True,  # fill with color
    #  labels=[]  # will be used to label x-ticks
)

bp2 = ax2.boxplot(
    list(test_deletion_commits_range.values())[6],
    showfliers=False,
    # notch=True,  # notch shape
    vert=False,  # vertical box alignment
    patch_artist=True,  # fill with color
    #  labels=[]  # will be used to label x-ticks
)

# Set boxes, whiskers and fliers config
plt.setp(bp1["boxes"], color="black")
plt.setp(bp2["boxes"], color="black")
plt.setp(bp1["whiskers"], color="black")
plt.setp(bp2["whiskers"], color="black")
# plt.setp(bp['fliers'], color='red', marker='+')

# Set colors
colors1 = [
    "pink",
    "lightblue",
    "lightgreen",
    "red",
    "blue",
    "brown",
]
colors2 = ["violet"]
for patch, color in zip(bp1["boxes"], colors1):
    patch.set_facecolor(color)

for patch, color in zip(bp2["boxes"], colors2):
    patch.set_facecolor(color)
# Add a vertical grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.xaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
ax2.xaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
# ax1.set(
#     axisbelow=True,  # Hide the grid behind plot objects
#     # title='No. of deleted tests per commit',
#     # ylabel="Projects",
#     xlabel="No. of commits",
# )
# ax2.set(
#     axisbelow=True,  # Hide the grid behind plot objects
#     # title='No. of deleted tests per commit',
#     # ylabel="Projects",
#     xlabel="No. of commits",
# )

# Set common labels
fig.text(0.56, 0.02, "No. of commits", ha="center", va="center")

# # Set the axes ranges and axes labels
# ax.set_xlim(0.5, 100)
# top = 40
# bottom = -5
# ax.set_ylim(bottom, top)
print(list(test_deletion_commits_range.keys()))
ax1.set_yticklabels(
    ["commons-lang", "commons-math", "pmd", "jfreechart", "gson", "joda-time"]
)
ax2.set_yticklabels(["cts"])

# Due to the Y-axis scale being different across samples, it can be
# hard to compare differences in medians across the samples. Add upper
# X-axis tick labels with the sample medians to aid in comparison
# (just use two decimal places of precision)
# pos = np.arange(7) + 1
# upper_labels = [str(round(s, 2)) for s in medians]
# weights = ["bold", "semibold"]
# for tick, label in zip(range(7), ax.get_yticklabels()):
#     k = tick % 2
#     ax.text(
#         pos[tick],
#         0.97,
#         upper_labels[tick],
#         transform=ax.get_yaxis_transform(),
#         horizontalalignment="center",
#         size="x-small",
#         #  weight=weights[k], color=box_colors[k]
#     )
fig.tight_layout()
# fig.savefig(OUT_DIR + "commits-interval-between-test-deletion-commits.png", dpi=800)
plt.show()
