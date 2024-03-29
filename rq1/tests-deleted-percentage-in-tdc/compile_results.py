"""
Compiles total % percentage of deleted tests across all test deletion commits for all projects in a single csv file
Results is then used by R to plot figures
"""

import os.path
from pathlib import Path
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn
import numpy as np


from pmd import data as pmd
from commons_lang import data as commons_lang
from commons_math import data as commons_math
from cts import data as cts
from jfreechart import data as jfreechart
from gson import data as gson
from joda_time import data as joda_time

projects_map = {
    "commons-lang": commons_lang,
    "gson": gson,
    "commons-math": commons_math,
    "joda-time": joda_time,
    "jfreechart": jfreechart,
    "pmd": pmd,
    "cts": cts,
}

results = []
for project, data in projects_map.items():
    for commit, meta in data.items():
        per_del = round(meta["Total Deleted"] / meta["Total tests"] * 100, 2)
        results.append([project, per_del])


# Export to csv
df = pd.DataFrame(results, columns=["Project", "Tests Deleted %"])
df.to_csv("percentage_of_tests_deleted_in_tdc.csv", index=False)
