import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

old_file="io/outputRevisedLatest2/pmd/pmd-step3_01-01-2000_01-01-2023.csv"
new_file="io/outputRevisedLatest3/pmd/pmd-step3_01-01-2000_01-01-2023.csv"

# Get testcases missing in new file and contained in old file
# with open(old_file, 'r') as a, open(new_file, 'r') as b:
#     old_file = list(csv.reader(a, delimiter=',') )
#     new_file = list(csv.reader(b, delimiter=',') )

#     alter = []
#     for old_testcase_data in old_file:
#         if old_testcase_data[1] == '':
#             continue
        
#         match_found = False
#         for new_testcase_data in new_file:
#             if old_testcase_data[1] == new_testcase_data[1]:
#                 match_found = True
#                 break
#         if not match_found:
#             alter.append([old_testcase_data[1]])

#     export_to_csv(headers=["Hash"], records=alter, filename="diff1", dir="io/outputRevisedLatest3/pmd")


# Get testcases missing in old file and contained in new file

with open(old_file, 'r') as a, open(new_file, 'r') as b:
    old_file = list(csv.reader(a, delimiter=',') )
    new_file = list(csv.reader(b, delimiter=',') )

    alter = []
    for new_testcase_data in new_file:
        if new_testcase_data[1] == '':
            continue
        
        match_found = False
        for each2 in old_file:
            if new_testcase_data[1] == each2[1]:
                match_found = True
                break
        if not match_found:
            alter.append([new_testcase_data[1]])

    export_to_csv(headers=["Hash"], records=alter, filename="diff2", dir="io/outputRevisedLatest3/pmd")
