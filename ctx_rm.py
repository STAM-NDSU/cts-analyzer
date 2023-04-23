import os.path
from pathlib import Path
import pandas as pd

# Customize for required projects

# # 1. CommonsLang
# INPUT_DIR = 'outputRevisedLatest/commons-lang'
# OUTPUT_FILE = 'commons_lang_analyzer.xlsx'
# files = [{"filename": "commons-lang-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "commons-lang-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "commons-lang-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# 2. Guava
# INPUT_DIR = 'outputRevisedLatest/guava'
# OUTPUT_FILE = 'guava_analyzer.xlsx'
# files = [{"filename": "guava-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "guava-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "guava-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 3. Tink
# INPUT_DIR = 'outputRevisedLatest/tink'
# OUTPUT_FILE = 'tink_analyzer.xlsx'
# files = [{"filename": "tink-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "tink-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "tink-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 4. Mug
# INPUT_DIR = 'outputRevisedLatest/mug'
# OUTPUT_FILE = 'mug_analyzer.xlsx'
# files = [{"filename": "mug-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "mug-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "mug-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 4. Joda Time
# INPUT_DIR = 'outputRevisedLatest/joda-time'
# OUTPUT_FILE = 'joda-time_analyzer.xlsx'
# files = [{"filename": "joda-time-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "joda-time-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "joda-time-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 5. Gitiles
# INPUT_DIR = 'outputRevisedLatest/gitiles'
# OUTPUT_FILE = 'gitiles_analyzer.xlsx'
# files = [{"filename": "gitiles-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "gitiles-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "gitiles-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 6. Accumulo
# INPUT_DIR = 'outputRevisedLatest/accumulo'
# OUTPUT_FILE = 'accumulo_analyzer.xlsx'
# files = [{"filename": "accumulo-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "accumulo-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "accumulo-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]
# def parse_filename(file, ext=True):
#     if ext:
#         file["filename"] += '.csv'
#     return file["filename"]

# # 7. Closure Compiler
# INPUT_DIR = 'outputRevisedLatest/closure-compiler'
# OUTPUT_FILE = 'closure-compiler_analyzer.xlsx'
# files = [{"filename": "closure-compiler-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "closure-compiler-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "closure-compiler-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 8. PMD
# INPUT_DIR = 'outputRevisedLatest/pmd'
# OUTPUT_FILE = 'pmd_analyzer.xlsx'
# files = [{"filename": "pmd-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "pmd-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "pmd-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 8. Gson
# INPUT_DIR = 'outputRevisedLatest/gson'
# OUTPUT_FILE = 'gson_analyzer.xlsx'
# files = [{"filename": "gson-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "gson-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "gson-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 9. Commons Math
# INPUT_DIR = 'outputRevisedLatest/commons-math'
# OUTPUT_FILE = 'commons-math_analyzer.xlsx'
# files = [{"filename": "commons-math-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "commons-math-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "commons-math-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# # 10. Jfreechart
# INPUT_DIR = 'outputRevisedLatest/jfreechart'
# OUTPUT_FILE = 'jfreechart_analyzer.xlsx'
# files = [{"filename": "jfreechart-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
#     {"filename": "jfreechart-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
#         {"filename": "jfreechart-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

# 11. CTS
INPUT_DIR = 'outputRevisedLatest/cts'
OUTPUT_FILE = 'cts_analyzer.xlsx'
files = [{"filename": "cts-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"}, \
    {"filename": "cts-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"}, \
        {"filename": "cts-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"}]

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
