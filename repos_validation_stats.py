import os.path
from pathlib import Path
import pandas as pd
import random
import csv

import sys

# Redirect console ouput to a file
sys.stdout = open("./stats/all_repos_validation_stat.txt", "w")


projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

all_total_conflicts_before_resolution = 0
all_total_yes_before_resolution = 0
all_total_no_before_resolution = 0
all_total_others_before_resolution = 0

all_total_suraj_yes_before_resolution = 0
all_total_suraj_no_before_resolution = 0
all_total_ajay_yes_before_resolution = 0
all_total_ajay_no_before_resolution = 0

all_total_conflicts_after_resolution = 0
all_total_yes_after_resolution = 0
all_total_no_after_resolution = 0
all_total_others_after_resolution = 0

all_total_observations = 0
            
for project in projects_list:

    def main(project):
        global all_total_conflicts_before_resolution
        global all_total_yes_before_resolution
        global all_total_no_before_resolution
        global all_total_others_before_resolution

        global all_total_suraj_yes_before_resolution
        global all_total_suraj_no_before_resolution
        global all_total_ajay_yes_before_resolution
        global all_total_ajay_no_before_resolution

        global all_total_conflicts_after_resolution
        global all_total_yes_after_resolution
        global all_total_no_after_resolution
        global all_total_others_after_resolution

        global all_total_observations
        
        print("Project: ", project)
        IO_DIR = "io/validationFiles"
        PROJECT = project
        validation_file = "validation_diff_done_hydrated.csv"
        full_file_path = Path(f"{IO_DIR}/{PROJECT}/{validation_file}")
        valid_tests_deletion_commits = []
        
        if os.path.exists(f"{full_file_path}"):
            df = pd.read_csv(f"{full_file_path}")

            total_conflicts_before_resolution = 0
            total_yes_before_resolution = 0
            total_no_before_resolution = 0
            total_others_before_resolution = 0

            total_suraj_yes_before_resolution = 0
            total_suraj_no_before_resolution = 0
            total_ajay_yes_before_resolution = 0
            total_ajay_no_before_resolution = 0
            
            total_conflicts_after_resolution = 0
            total_yes_after_resolution = 0
            total_no_after_resolution = 0
            total_others_after_resolution = 0
           
            total_observations = df.shape[0]
            all_total_observations +=total_observations
            
            print("Total obervations: ", total_observations)
            for index, row in df.iterrows():
                if row["Manual Validation"] == "conflict":
                    total_conflicts_before_resolution += 1
                    all_total_conflicts_before_resolution += 1
                   
                elif row["Manual Validation"] == "yes":
                    total_yes_before_resolution += 1
                    all_total_yes_before_resolution += 1
                elif row["Manual Validation"] == "no":
                    total_no_before_resolution += 1
                    all_total_no_before_resolution += 1
                else:
                    total_others_before_resolution += 1
                    all_total_others_before_resolution += 1

                if row["Suraj Manual Validation"] == "yes": 
                    total_suraj_yes_before_resolution +=1
                    all_total_suraj_yes_before_resolution +=1
                elif row["Suraj Manual Validation"] == "no":
                   total_suraj_no_before_resolution +=1
                   all_total_suraj_no_before_resolution +=1
                
                if row["Ajay Manual Validation"] == "yes":
                    total_ajay_yes_before_resolution +=1
                    all_total_ajay_yes_before_resolution +=1
                if row["Ajay Manual Validation"] == "no":
                    total_ajay_no_before_resolution +=1
                    all_total_ajay_no_before_resolution +=1
                    
                if row["Final Results"] == "conflict":
                    total_conflicts_after_resolution += 1
                    all_total_conflicts_after_resolution += 1
                elif row["Final Results"] == "yes":
                    total_yes_after_resolution += 1
                    all_total_yes_after_resolution += 1
                    valid_tests_deletion_commits.append(row['Hash'])
                elif row["Final Results"] == "no":
                    total_no_after_resolution += 1
                    all_total_no_after_resolution += 1
                else:
                    print(row['Hash'])
                    total_others_after_resolution += 1
                    all_total_others_after_resolution += 1

            valid_tests_deletion_commits = list({*valid_tests_deletion_commits})
            print("Total Valid Tests Deletion Commits: ",  len(valid_tests_deletion_commits))
            print(
                "total_conflicts_before_resolution: ", total_conflicts_before_resolution
            )
            print("total_yes_before_resolution: ", total_yes_before_resolution)
            print("total_no_before_resolution: ", total_no_before_resolution)
            print("total_others_before_resolution: ", total_others_before_resolution)

            print(
                "total_conflicts_after_resolution: ", total_conflicts_after_resolution
            )
            print("total_yes_after_resolution: ", total_yes_after_resolution)
            print("total_no_after_resolution: ", total_no_after_resolution)
            print("total_others_after_resolution: ", total_others_after_resolution)
            
            
            print("-----Kappa's score")
            print("total_suraj_yes_before_resolution :", total_suraj_yes_before_resolution)
            print("total_suraj_no_before_resolution :", total_suraj_no_before_resolution)
            print("total_ajay_yes_before_resolution :", total_ajay_yes_before_resolution)
            print("total_ajay_no_before_resolution :", total_ajay_no_before_resolution)
            
            
            """
            K = (Observed agreement - chance agreement) / (1-chance agreement)
            observed agreement = (total no conflicts)/total observations
            chance agreement = probability of both saying yes + prob of both saying no
            """
            total_no_conflicts = total_observations - total_conflicts_before_resolution
            observed_agreement = total_no_conflicts / total_observations
            chance_yes_agreement  = (total_suraj_yes_before_resolution/total_observations) * (total_ajay_yes_before_resolution/total_observations)
            chance_no_agreement  = (total_suraj_no_before_resolution/total_observations) * (total_ajay_no_before_resolution/total_observations)
            chance_agreement =chance_yes_agreement + chance_no_agreement
            k = (observed_agreement- chance_agreement) / (1-chance_agreement)
            print("Kappa's score: ", k)
            print("================================================================")

    main(project)
    
print("Final Results")
print("Total observations: ", all_total_observations)
print(
    "all_total_conflicts_before_resolution: ", all_total_conflicts_before_resolution
)
print("all_total_yes_before_resolution: ", all_total_yes_before_resolution)
print("all_total_no_before_resolution: ", all_total_no_before_resolution)
print("all_total_others_before_resolution: ", all_total_others_before_resolution)

print(
    "all_total_conflicts_after_resolution: ", all_total_conflicts_after_resolution
)
print("all_total_yes_after_resolution: ", all_total_yes_after_resolution)
print("all_total_no_after_resolution: ", all_total_no_after_resolution)
print("all_total_others_after_resolution: ", all_total_others_after_resolution)

print("----- Final Kappa's score")
print("all_total_suraj_yes_before_resolution :", all_total_suraj_yes_before_resolution)
print("all_total_suraj_no_before_resolution :", all_total_suraj_no_before_resolution)
print("all_total_ajay_yes_before_resolution :", all_total_ajay_yes_before_resolution)
print("all_total_ajay_no_before_resolution :", all_total_ajay_no_before_resolution)


"""
K = (Observed agreement - chance agreement) / (1-chance agreement)
observed agreement = (total no conflicts)/total observations
chance agreement = probability of both saying yes + prob of both saying no
"""
total_no_conflicts = all_total_observations - all_total_conflicts_before_resolution
observed_agreement = total_no_conflicts / all_total_observations
chance_yes_agreement  = (all_total_suraj_yes_before_resolution/all_total_observations) * (all_total_ajay_yes_before_resolution/all_total_observations)
chance_no_agreement  = (all_total_suraj_no_before_resolution/all_total_observations) * (all_total_ajay_no_before_resolution/all_total_observations)
chance_agreement =chance_yes_agreement + chance_no_agreement
k = (observed_agreement- chance_agreement) / (1-chance_agreement)
print("Final Kappa's score: ", k)
print("================================================================")
