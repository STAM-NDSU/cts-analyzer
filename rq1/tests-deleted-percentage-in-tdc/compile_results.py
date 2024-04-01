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

all_results = []
for project, data in projects_map.items():
    results = []
    for commit, meta in data.items():
        total_tests = meta["Total tests"]
        total_del = meta["Total Deleted"]
        per_del = round(total_del / total_tests * 100, 2)
        results.append([project, total_tests, total_del, per_del])
        all_results.append([project, total_tests, total_del, per_del])


    # Export to csv
    df = pd.DataFrame(results, columns=["Project", "Total Tests", "Total Tests Deleted",  "Tests Deleted in %"])
    df.to_csv(f"{project}.csv", index=False)
    
# Export to csv
df = pd.DataFrame(all_results, columns=["Project", "Total Tests", "Total Tests Deleted",  "Tests Deleted in %"])
df.to_csv("percentage_of_tests_deleted_in_tdc.csv", index=False)
