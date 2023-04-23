import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

file1="io/outputRevisedLatest/commons-lang/new.csv"
file2="io/outputRevisedLatest/commons-lang/original.csv"

with open(file1, 'r') as a, open(file2, 'r') as b:
    file1 = csv.reader(a, delimiter=',') 
    file2 = csv.reader(b, delimiter=',') 

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

    export_to_csv(headers=["Hash"], records=alter, filename="diff", dir="io/outputRevisedLatest/commons-lang")
