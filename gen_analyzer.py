import os.path
from pathlib import Path
import pandas as pd

# Customize for required projects

PROJECTS = [
    {
        # 1. CommonsLang
        "input_dir": "io/outputRevisedLatest3/commons-lang",
        "ouput_file": "commons_lang_analyzer.xlsx",
        "files": [
            {
                "filename": "commons-lang-step1_01-01-2000_01-01-2023",
                "excel_filename": "step 1",
            },
            {
                "filename": "commons-lang-step2_01-01-2000_01-01-2023",
                "excel_filename": "step 2",
            },
            {
                "filename": "commons-lang-step3_01-01-2000_01-01-2023",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 2. Joda Time
        "input_dir": "io/outputRevisedLatest3/joda-time",
        "ouput_file": "joda-time_analyzer.xlsx",
        "files": [
            {
                "filename": "joda-time-step1_01-01-2000_01-01-2023",
                "excel_filename": "step 1",
            },
            {
                "filename": "joda-time-step2_01-01-2000_01-01-2023",
                "excel_filename": "step 2",
            },
            {
                "filename": "joda-time-step3_01-01-2000_01-01-2023",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 3. PMD
        "input_dir": "io/outputRevisedLatest3/pmd",
        "ouput_file": "pmd_analyzer.xlsx",
        "files": [
            {"filename": "pmd-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"},
            {"filename": "pmd-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"},
            {"filename": "pmd-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"},
        ],
    },
    {
        # 4. Gson
        "input_dir": "io/outputRevisedLatest3/gson",
        "ouput_file": "gson_analyzer.xlsx",
        "files": [
            {
                "filename": "gson-step1_01-01-2000_01-01-2023",
                "excel_filename": "step 1",
            },
            {
                "filename": "gson-step2_01-01-2000_01-01-2023",
                "excel_filename": "step 2",
            },
            {
                "filename": "gson-step3_01-01-2000_01-01-2023",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 5. Commons Math
        "input_dir": "io/outputRevisedLatest3/commons-math",
        "ouput_file": "commons-math_analyzer.xlsx",
        "files": [
            {
                "filename": "commons-math-step1_01-01-2000_01-01-2023",
                "excel_filename": "step 1",
            },
            {
                "filename": "commons-math-step2_01-01-2000_01-01-2023",
                "excel_filename": "step 2",
            },
            {
                "filename": "commons-math-step3_01-01-2000_01-01-2023",
                "excel_filename": "step 3",
            },
        ],
    },
    {
        # 6. Jfreechart
        "input_dir": "io/outputRevisedLatest3/jfreechart",
        "ouput_file": "jfreechart_analyzer.xlsx",
        "files": [
            {
                "filename": "jfreechart-step1_01-01-2000_01-01-2023",
                "excel_filename": "step 1",
            },
            {
                "filename": "jfreechart-step2_01-01-2000_01-01-2023",
                "excel_filename": "step 2",
            },
            {
                "filename": "jfreechart-step3_01-01-2000_01-01-2023",
                "excel_filename": "step 3",
            },
        ],
    },
    # {
    #     # 7. CTS
    #     "input_dir": "io/outputRevisedLatest3/cts",
    #     "ouput_file": "cts_analyzer.xlsx",
    #     "files": [
    #         {"filename": "cts-step1_01-01-2000_01-01-2023", "excel_filename": "step 1"},
    #         {"filename": "cts-step2_01-01-2000_01-01-2023", "excel_filename": "step 2"},
    #         {"filename": "cts-step3_01-01-2000_01-01-2023", "excel_filename": "step 3"},
    #     ],
    # },
]


def parse_filename(file, ext=True):
    if ext:
        file["filename"] += ".csv"
    return file["filename"]


for each in PROJECTS:
    files = each["files"]
    input_dir = each["input_dir"]
    ouput_file = each["ouput_file"]
    parsed_filenames = list(map(parse_filename, files))
    writer = pd.ExcelWriter(f"{input_dir}/{ouput_file}", engine="xlsxwriter")

    for index, filename in enumerate(parsed_filenames):
        file_path = Path(f"{input_dir}/{filename}")

        if os.path.exists(f"{input_dir}/{filename}"):
            df = pd.read_csv(f"{input_dir}/{filename}")
            sheet_name = files[index]["excel_filename"]
            print(ouput_file, sheet_name)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()
