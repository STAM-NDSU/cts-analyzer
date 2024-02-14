"""
Generate stacked vertical bargraphs for obsolte(deleted with source code) and redundant (without source code) tests [rq2]
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 6})
projects = (
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
)
deleted_tests = {
    "Obsolete": [546, 197, 2090, 98, 191, 897, 0],
    "Redundant": [323, 63, 1226, 53, 469, 1173, 0],
    "All": [0, 0, 0, 0, 0, 0, 17105],
}
total_deleted_tests = [869, 260, 3316, 151, 660, 2070, 17105]
labels = {
    "Obsolete": "Obsolete tests",
    "Redundant": "Redundant tests",
    "All": "Obsolete and Redundant tests",
}
colors = {"Obsolete": "orange", "Redundant": "green", "All": "grey"}
width = 0.5

fig, ax = plt.subplots(figsize=(3.5, 3))

bottom = np.zeros(7)


for index, (project, tests_count) in enumerate(deleted_tests.items()):
    pps = ax.bar(
        projects,
        tests_count,
        width,
        label=labels[project],
        bottom=bottom,
        color=colors[project],
        align="center",  # controls where bars should be palced above ticks
    )
    # Calculates the bottom position of the bar next in the stack
    bottom += tests_count
    
    # Add a single text label to the top of each bar
    if index == 2:
        for i, value in enumerate(tests_count):
            ax.text(
                i, # x-cordinate value
                bottom[i]  + 100, # y-cordinate,
                total_deleted_tests[i], # Get the total deleted tests for ith project
                ha="center",
                va="bottom",
                fontsize=5,
                color="black",
            )

    # for i, p in enumerate(pps):
    #     if(i==2):
    #         height = p.get_height()
    #         ax.text(x=p.get_x() + p.get_width() / 2, y=height+.10,
    #         s="{}".format(height),
    #         ha='center', fontsize=5)
    # ax.text(i, bottom[i] + value + 1, "hello", ha='center', va='bottom')

# ax.set_title("Number of deleted tests")
plt.ylabel("Number of deleted tests")
ax.legend(loc="upper left", fontsize=5)
plt.xticks(rotation=15, fontsize=5)
plt.gcf().subplots_adjust(left=0.15, bottom=0.11, top=0.98, right=1, hspace=0, wspace=0)

# plt.show()
OUT_DIR = "../io/rq2/figures/"
fig.savefig(OUT_DIR + "deleted_with_source_code2.pdf", dpi=1200)
