import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

file1="io/outputRevisedLatest2/pmd/pmd-step3_01-01-2000_01-01-2023.csv"
file2="io/outputRevisedLatest/pmd/pmd-step3_01-01-2000_01-01-2023.csv"

with open(file1, 'r') as a, open(file2, 'r') as b:
    file1 = list(csv.reader(a, delimiter=',') )
    file2 = list(csv.reader(b, delimiter=',') )

    alter = []
    for each1 in file1:
        if each1[1] != '':
            match_found = False
            for each2 in file2:
                if each1[1] == each2[1]:
                    match_found = True
                    break
            if not match_found:
                alter.append([each1[1]])

    export_to_csv(headers=["Hash"], records=alter, filename="diff1", dir="io/outputRevisedLatest2/pmd")


# with open(file1, 'r') as a, open(file2, 'r') as b:
#     file1 = list(csv.reader(a, delimiter=',') )
#     file2 = list(csv.reader(b, delimiter=',') )

#     alter = []
#     for each1 in file2:
#         if each1[1] != '':
#             match_found = False
#             for each2 in file1:
#                 if each1[1] == each2[1]:
#                     match_found = True
#                     break
#             if not match_found:
#                 alter.append([each1[1]])

#     export_to_csv(headers=["Hash"], records=alter, filename="diff2", dir="io/outputRevisedLatest2/pmd")
