import os.path
from pathlib import Path
import pandas as pd

# Customize for required projects

root_dir = "io/outputRevisedLatest4/"


projects = [
    {
        # 1. CommonsLang
        "INPUT_DIR": "commons-lang",
        "OUTPUT_FILE": "commons_lang_analyzer.xlsx",
        "files": [
            {
                "filename": "commons-lang-step1",
                "excel_filename": "step 1",
            },
            {
                "filename": "commons-lang-step11",
                "excel_filename": "step 11",
            },
            {
                "filename": "commons-lang-step2",
                "excel_filename": "step 2",
            },
            {
                "filename": "commons-lang-step3",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 2. Joda Time
        "INPUT_DIR": "joda-time",
        "OUTPUT_FILE": "joda-time_analyzer.xlsx",
        "files": [
            {
                "filename": "joda-time-step1",
                "excel_filename": "step 1",
            },
            {
                "filename": "joda-time-step11",
                "excel_filename": "step 11",
            },
            {
                "filename": "joda-time-step2",
                "excel_filename": "step 2",
            },
            {
                "filename": "joda-time-step3",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 3. PMD
        "INPUT_DIR": "pmd",
        "OUTPUT_FILE": "pmd_analyzer.xlsx",
        "files": [
            {"filename": "pmd-step1", "excel_filename": "step 1"},
            {"filename": "pmd-step11", "excel_filename": "step 11"},
            {"filename": "pmd-step2", "excel_filename": "step 2"},
            {"filename": "pmd-step3", "excel_filename": "step 3"},
        ],
    },
    {
        # 4. Gson
        "INPUT_DIR": "gson",
        "OUTPUT_FILE": "gson_analyzer.xlsx",
        "files": [
            {
                "filename": "gson-step1",
                "excel_filename": "step 1",
            },
               {
                "filename": "gson-step11",
                "excel_filename": "step 11",
            },
            {
                "filename": "gson-step2",
                "excel_filename": "step 2",
            },
            {
                "filename": "gson-step3",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 5. Commons Math
        "INPUT_DIR": "commons-math",
        "OUTPUT_FILE": "commons-math_analyzer.xlsx",
        "files": [
            {
                "filename": "commons-math-step1",
                "excel_filename": "step 1",
            },
            {
                "filename": "commons-math-step11",
                "excel_filename": "step 11",
            },
            {
                "filename": "commons-math-step2",
                "excel_filename": "step 2",
            },
            {
                "filename": "commons-math-step3",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 6. Jfreechart
        "INPUT_DIR": "jfreechart",
        "OUTPUT_FILE": "jfreechart_analyzer.xlsx",
        "files": [
            {
                "filename": "jfreechart-step1",
                "excel_filename": "step 1",
            },
             {
                "filename": "jfreechart-step11",
                "excel_filename": "step 11",
            },
            {
                "filename": "jfreechart-step2",
                "excel_filename": "step 2",
            },
            {
                "filename": "jfreechart-step3",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 7. CTS
        "INPUT_DIR": "cts",
        "OUTPUT_FILE": "cts_analyzer.xlsx",
        "files": [
            {"filename": "cts-step1", "excel_filename": "step 1"},
               {"filename": "cts-step11", "excel_filename": "step 11"},
            {"filename": "cts-step2", "excel_filename": "step 2"},
            {"filename": "cts-step3", "excel_filename": "step 3"},
        ],
    },
]


def parse_filename(file):
    return file["filename"] + ".csv"


for project_info in projects:
    files = project_info["files"]
    input_dir = root_dir + project_info["INPUT_DIR"]
    output_file = project_info["OUTPUT_FILE"]
    parsed_filenames = list(map(parse_filename, files))
    writer = pd.ExcelWriter(f"{root_dir}/{output_file}", engine="xlsxwriter")

    for index, filename in enumerate(parsed_filenames):
        file_path = Path(f"{input_dir}/{filename}")

        if os.path.exists(f"{input_dir}/{filename}"):
            df = pd.read_csv(f"{input_dir}/{filename}")
            sheet_name = files[index]["excel_filename"]
            print(input_dir, sheet_name)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()
