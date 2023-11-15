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
    "bcd": [688, 226, 2738, 122, 291, 1548, 14723],
    "~bcd": [181, 34, 578, 29, 369, 522, 2382],
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
plt.xlabel("Total Deleted Tests")
plt.ylabel("Projects")
ax.legend(["Deleted with Test Class", "Deleted without Test Class"])


# function to add value labels
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha="center")


# addlabels(df["projects"], df["bcd"])
plt.gcf().subplots_adjust(left=0.25, bottom=0.2)
fig.savefig(OUT_DIR + "deleted_with_test_class.png", dpi=800)
plt.show()
