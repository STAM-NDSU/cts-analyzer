"""
Generate bargraphs for deleted tests and test deletion commits patterns [rq2]
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

plt.rcParams.update({"font.size": 16})

OUT_DIR = "../io/rq2/figures/"
fig, ax = plt.subplots(figsize=(7, 3.5))

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
colors = {"Obsolete": "orange", "Redundant": "green"}
width = 0.6

# Create an array of project indices for the x-axis
indices = np.arange(len(projects))

fig, ax = plt.subplots(figsize=(6, 3.5))

# Plot each category as a stacked horizontal bar
bottom = np.zeros(len(projects))
for index, (category, values) in enumerate(deleted_tests.items()):
    ax.barh(
        projects,
        values,
        label=labels[category],
        left=bottom,
        color=colors[category],
        height=width,
        align="center",
    )
    bottom += values
    


plt.xlabel("Number of deleted tests")
plt.ylabel("")
ax.legend(["Obsolete tests", "Redundant tests"], loc="lower right")


# function to add value labels
# def addlabels(x, y):
#     for i in range(len(x)):
#         plt.text(i, y[i], y[i], ha="center")

# addlabels(df_rq21["projects"], df_rq21["abc"])

# plt.gcf().subplots_adjust(left=0, bottom=0.2,  top=1, right=1, hspace = 0, wspace = 0)
# plt.margins(0,0)
fig.savefig(OUT_DIR + "deleted_with_source_code00.pdf", dpi=1200, bbox_inches="tight")
fig.savefig(OUT_DIR + "deleted_with_source_code00.png", dpi=1200, bbox_inches="tight")
# plt.show()
