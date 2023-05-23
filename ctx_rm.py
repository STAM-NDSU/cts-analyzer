import os.path
from pathlib import Path
import pandas as pd

# Customize for required projects

# # 1. CommonsLang
# INPUT_DIR = 'io/outputRevisedLatest2/commons-lang'
# OUTPUT_FILE = 'commons_lang_analyzer.xlsx'
# files = [{"filename": "commons-lang-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "commons-lang-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "commons-lang-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 2. Joda Time
# INPUT_DIR = 'io/outputRevisedLatest2/joda-time'
# OUTPUT_FILE = 'joda-time_analyzer.xlsx'
# files = [{"filename": "joda-time-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "joda-time-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "joda-time-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 3. PMD
# INPUT_DIR = 'io/outputRevisedLatest2/pmd'
# OUTPUT_FILE = 'pmd_analyzer.xlsx'
# files = [{"filename": "pmd-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "pmd-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "pmd-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 4. Gson
# INPUT_DIR = 'io/outputRevisedLatest2/gson'
# OUTPUT_FILE = 'gson_analyzer.xlsx'
# files = [{"filename": "gson-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "gson-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "gson-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# 5. Commons Math
INPUT_DIR = 'io/outputRevisedLatest2/commons-math'
OUTPUT_FILE = 'commons-math_analyzer.xlsx'
files = [{"filename": "commons-math-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
    {"filename": "commons-math-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
        {"filename": "commons-math-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 6. Jfreechart
# INPUT_DIR = 'io/outputRevisedLatest2/jfreechart'
# OUTPUT_FILE = 'jfreechart_analyzer.xlsx'
# files = [{"filename": "jfreechart-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "jfreechart-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "jfreechart-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 7. CTS
# INPUT_DIR = 'io/outputRevisedLatest2/cts'
# OUTPUT_FILE = 'cts_analyzer.xlsx'
# files = [{"filename": "cts-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "cts-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "cts-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

def parse_filename(file, ext=True):
    if ext:
        file["filename"] += '.csv'
    return file["filename"]

parsed_filenames = list(map(parse_filename, files))
writer = pd.ExcelWriter(f'{INPUT_DIR}/{OUTPUT_FILE}', engine='xlsxwriter')

for index, filename in enumerate(parsed_filenames):
    file_path = Path(f'{INPUT_DIR}/{filename}')

    if os.path.exists(f'{INPUT_DIR}/{filename}'):
        df = pd.read_csv(f'{INPUT_DIR}/{filename}')
        sheet_name = files[index]["excel_filename"]
        print(sheet_name)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

writer.close()
