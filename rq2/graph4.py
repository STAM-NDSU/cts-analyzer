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

plt.rcParams["figure.autolayout"] = True
plt.rcParams.update({"font.size": 6.5})

OUT_DIR = "../io/rq2/figures/"

data = {
    "projects": [
        "commons-lang",
        "gson",
        "commons-math",
        "jfreechart",
        "joda-time",
        "pmd",
        "cts",
    ],
    "bcd": [38, 23, 105, 9, 7, 37, 427],
    "~bcd": [70, 14, 126, 5, 24, 179, 961],
}
fig, ax = plt.subplots(figsize=(4, 2))
df = pd.DataFrame(data)
df.plot(
    x="projects",
    kind="barh",
    stacked=True,
    color={"bcd": "orange", "~bcd": "green"},
    width=0.4,
    ax=ax
    # title="Stacked Bar Graph by dataframe"
)
plt.xlabel("Total Test Deletion Commits")
plt.ylabel("Projects")
ax.legend(["Delete Multiple Test Classes", "Delete Single Test Class"])


# function to add value labels
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha="center")


# addlabels(df["projects"], df["bcd"])

# ax.set_ylim(0)
# ax.set_xlim(0)
plt.gcf().subplots_adjust(left=0.22, bottom=0.2)
# plt.margins(x=0, y=0)
# fig.tight_layout(pad=5)
fig.savefig(OUT_DIR + "delete_multiple_test_class.png", dpi=800)
plt.show()
