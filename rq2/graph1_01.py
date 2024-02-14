"""
Generate stacked horizontal bargraphs for obsolte(deleted with source code) and redundant (without source code) tests [rq2]
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

plt.rcParams.update({"font.size": 6})

OUT_DIR = "../io/rq2/figures/"

df_rq21 = {
    "projects": [
        "commons-lang",
        "gson",
        "commons-math",
        "jfreechart",
        "joda-time",
        "pmd",
        "cts",
    ],
    "obsolete": [546, 197, 2090, 98, 191, 897, 0],
    "redundant": [323, 63, 1226, 53, 469, 1173, 0],
    "all": [0, 0, 0, 0, 0, 0, 17105],
}
total_deleted_tests = [869, 260, 3316, 151, 660, 2070, 17105]
fig, ax = plt.subplots(figsize=(3.5, 2))
df_rq21 = pd.DataFrame(df_rq21)
df_rq21.plot(
    x="projects",
    kind="barh",
    stacked=True,
    color={"obsolete": "orange", "redundant": "green", "all": "grey"},
    width=0.4,
    ax=ax,
    # title="Stacked Bar Graph by dataframe"
)
for i, value in enumerate(total_deleted_tests):
    if i == 6: # Modify for CTS (lower down the y co-ordinate)
        ax.text(
            value - 1200,  # x-cordinate,
            i-0.5,  # y-cordinate value
            value,  # Get the total deleted tests for ith project
            # ha="center",
            va="center",
            fontsize=5,
            color="black",
        )
    else:
        ax.text(
            value + 200,  # x-cordinate,
            i,  # y-cordinate value
            value,  # Get the total deleted tests for ith project
            ha="left",
            va="center",
            fontsize=5,
            color="black",
        )

plt.xlabel("Number of deleted tests")
plt.ylabel("")
ax.legend(["Obsolete tests", "Redundant tests", "Obsolete and Redundant tests"], fontsize=5)
plt.yticks(rotation=15, fontsize=5)

# # function to add value labels
# def addlabels(x, y):
#     for i in range(len(x)):
#         plt.text(i, y[i], y[i], ha="center")

# addlabels(df_rq21["projects"], df_rq21["abc"])

plt.gcf().subplots_adjust(left=0.2, bottom=0.2, top=1, right=1, hspace=0.2, wspace=0)
# plt.margins(0,0)
fig.savefig(OUT_DIR + "deleted_with_source_code.pdf", dpi=1200)
# plt.show()
