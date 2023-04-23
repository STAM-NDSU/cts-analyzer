import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

file1="outputCommonLangRevised/cts_01-01-2000_01-01-2023.csv"
file2="outputCommonLang/commons-lang-wRM_01-01-2000_01-01-2023.csv"

with open(file1, 'r') as a, open(file2, 'r') as b:
    file1 = csv.reader(a, delimiter=',') 
    file2 = csv.reader(b, delimiter=',') 

    alter = []
    for each1 in file1:
        match_found = False
        for each2 in file2:
            if each1[4] == each2[4]:
                print([each1[1], each1[4]])
                match_found = True
                break
        if not match_found:
            alter.append([each1[1], each1[4]])

    export_to_csv(headers=["Hash", "Testcase"], records=alter, filename="diff", dir="outputCommonLang")
