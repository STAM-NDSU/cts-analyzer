"""
Combine piechart and bargraphs for deleted tests [rq2]
"""

import os.path
from pathlib import Path
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from collections import defaultdict
import seaborn as sns

plt.rcParams.update({"font.size": 10})
OUT_DIR = "../io/rq2/figures/"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,2.5), width_ratios=[ 90, 100])

# 1st Figure
# Data
deleted_tests = [260, 3316, 869, 660, 2070, 151, 17105]
labels = [
    "gson (260)",
    "commons-math (3,316)",
    "commons-lang (869)",
    "joda-time (660)",
    "pmd (2,070)",
    "jfreechart (151)",
    "cts (17,105)",
]
# Set a custom color palette for a more sophisticated look``
colors = sns.color_palette("deep")

def func(pct, allvals):
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return f"{absolute:d}"
ax1.pie(
    deleted_tests,
    labels=labels,
    # autopct=lambda pct: func(pct, deleted_tests),
    # pctdistance=0.75,
    startangle=275,
    colors=colors,
    # textprops={"fontsize": 8},
)


# 2nd figure
projects = (
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
)
deleted_tests = {
    "Obsolete": [546, 197, 2090, 98, 191, 897],
    "Redundant": [323, 63, 1226, 53, 469, 1173],
}
labels = {
    "Obsolete": "Obsolete tests",
    "Redundant": "Redundant tests",
}
colors = {"Obsolete": "orange", "Redundant": "green", "All": "grey"}
width = 0.6

projects = (
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
)

deleted_tests = {
    "Obsolete": [546, 197, 2090, 98, 191, 897],
    "Redundant": [323, 63, 1226, 53, 469, 1173],
}

labels = {
    "Obsolete": "Obsolete tests",
    "Redundant": "Redundant tests",
}

# Create an array of project indices for the x-axis
indices = np.arange(len(projects))

# Plot each category as a stacked horizontal bar
bottom = np.zeros(len(projects))
for index, (category, values) in enumerate(deleted_tests.items()):
    ax2.barh(
        projects,
        values,
        label=labels[category],
        left=bottom,
        color=colors[category],
        height=width,
        align="center",
    )
    bottom += values

# Set labels and legend
ax2.set_xlabel("Number of deleted tests")
ax2.set_yticks(indices)
ax2.set_yticklabels(projects)
ax2.legend(["Obsolete tests", "Redundant tests"], loc="lower right")

###########

# bottom = np.zeros(len(projects))
# # Plot each category as a stacked bar
# for index, (label, tests) in enumerate(deleted_tests.items()):
#     ax2.barh(projects, tests, label=labels[label], bottom=bottom[index])
#     bottom += tests

# # for index, (project, tests_count) in enumerate(deleted_tests.items()):
# #     pps = ax2.barh(
# #         projects,
# #         tests_count,
# #         width,
# #         label=labels[project],
# #         bottom=bottom,
# #         color=colors[project],
# #         align="center",  # controls where bars should be palced above ticks
# #     )
# #     # Calculates the bottom position of the bar next in the stack
# #     bottom += tests_count

# # Add labels and legend
# ax2.set_xlabel("Number of deleted tests")
# ax2.set_ylabel("")
# ax2.legend(["Obsolete tests", "Redundant tests"], loc="lower right")

# subplot parameters
# sp = dict(right=0.98, left=0.25, bottom=0.1, top=0.9, wspace=0.25, hspace=0.1)
# plt.subplots_adjust(**sp)

fig.tight_layout()

fig.savefig(
    OUT_DIR + "deleted_tests_and_with_without_source_code.pdf",
    dpi=1200,
    bbox_inches="tight",
)
fig.savefig(
    OUT_DIR + "deleted_tests_and_with_without_source_code.png",
    dpi=1200,
    bbox_inches="tight",
)
# plt.show()
