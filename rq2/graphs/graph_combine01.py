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

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4,4), height_ratios=[ 1, 1],)

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
    startangle=135,
    colors=colors,
    # frame=True
    # textprops={"fontsize": 8},
)
ax1.set_xmargin(10) 
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_ylabel('')

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
# ax2.set_yticks(indices)
# ax2.set_yticklabels(projects)
ax2.legend(["Obsolete tests", "Redundant tests"], loc="lower right")

# Add labels and legend
ax2.set_xlabel("Number of deleted tests")
ax2.set_ylabel("")
ax2.legend(["Obsolete tests", "Redundant tests"], loc="lower right")

# subplot parameters
sp = dict(right=0.9, left=0.1, bottom=0.1, top=1, wspace=0.2, hspace=0.1)
plt.subplots_adjust(**sp)

# fig.tight_layout(pad=1)

fig.savefig(
    OUT_DIR + "deleted_tests_and_with_without_source_code01.pdf",
    dpi=1200,
    bbox_inches="tight",
)
fig.savefig(
    OUT_DIR + "deleted_tests_and_with_without_source_code01.png",
    dpi=1200,
    bbox_inches="tight",
)
# plt.show()
