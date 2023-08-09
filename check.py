import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

old_file = "io/validationFiles/cts/validation_diff_done_hydrated.csv"
new_file = "io/validationFiles/cts/hydrated_rq_2.csv"

CSV_HEADERS = [
    "Datetime",
    "Hash",
    "Author",
    "Commit Msg",
    "Filepath",
    "Filename",
    "Removed Test Case",
    "Manual Validation",
    "Final Results",
]

# Get testcases missing in new file and contained in old file
with open(old_file, "r") as a, open(new_file, "r") as b:
    old_file = list(csv.reader(a, delimiter=","))
    new_file = list(csv.reader(b, delimiter=","))

    alter = []
    for old_testcase_data in old_file:
        if old_testcase_data[1] == "":  # check for hash
            continue

        if old_testcase_data[8] == "no":  # check only for truly removed one
            continue

        match_found = False
        match_found_no = 0
        for new_testcase_data in new_file:
            # if old_testcase_data[1] == new_testcase_data[1]:
            if (
                old_testcase_data[1] == new_testcase_data[1]
                and old_testcase_data[4] == new_testcase_data[4]
                and old_testcase_data[6] == new_testcase_data[6]
            ):
                
                match_found = True
                match_found_no += 1
                
        if not match_found or match_found_no > 1:
            alter.append([*old_testcase_data[: len(CSV_HEADERS)]])

    export_to_csv(
        headers=CSV_HEADERS,
        records=alter,
        filename="diff",
        dir="io/validationFiles/cts",
    )


# Get testcases missing in old file and contained in new file

# with open(old_file, 'r') as a, open(new_file, 'r') as b:
#     old_file = list(csv.reader(a, delimiter=',') )
#     new_file = list(csv.reader(b, delimiter=',') )

#     alter = []
#     for new_testcase_data in new_file:
#         if new_testcase_data[1] == '':
#             continue
#         print(new_testcase_data[1])

#         match_found = False
#         for each2 in old_file:
#             if new_testcase_data[1] == each2[1]:
#                 match_found = True
#                 break
#         if not match_found:
#             alter.append([new_testcase_data[1]])

#     export_to_csv(headers=["Hash"], records=alter, filename="clean2_vs_1_diff", dir="io/validationFiles4/cts")
