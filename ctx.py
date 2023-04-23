import pandas as pd
import os.path
from pathlib import Path

INPUT_DIR = 'io/outputCts'
OUTPUT_FILE = 'cts_analyzer.xlsx'

# Keep in sync with .sh file
files = ["08/15/2022-02/06/2023-v_13.0.0",
         "03/07/2022-08/15/2022-v_13.0.0",
         "10/04/2021-03/07/2022-v_12.1.0",
         "09/07/2020-07/29/2021-v_12.0.0_part1",
         "07/30/2021-09/28/2021-v_12.0.0_part2",
         "09/29/2021-10/04/2021-v_12.0.0_part3",  # 09/07/2020-10/04/2021
         "08/23/2019-09/07/2020-v_11.0.0",
         "07/24/2018-08/23/2019-v_10.0.0",
         "12/05/2017-07/24/2018-v_9.0.0",
         "08/21/2017-12/05/2017-v_8.1.0",
         "10/20/2016-08/21/2017-v_8.0.0",
         "08/22/2016-10/20/2016-v_7.1.0",
         "10/02/2015-08/22/2016-v_7.0.0",
         "03/02/2015-10/02/2015-v_6.0.0",
         "11/04/2014-03/02/2015-v_5.1.0",
         "10/30/2013-11/04/2014-v_5.0.0",
         "07/23/2013-10/30/2013-v_4.4",
         "11/13/2012-07/23/2013-v_4.3",
         "07/09/2012-11/13/2012-v_4.2",
         "12/16/2011-07/09/2012-v_4.1.1",
         "12/17/2010-12/16/2011-v_4.0.3",
         "06/29/2010-12/17/2010-v_2.3",
         "02/01/2010-06/29/2010-v_2.2",
         "01/01/2009-02/01/2010-v_2.1"]


def parse_filename(file, ext=True):
    raw = file.split("-")
    new_name = raw[2] + '_' + raw[0].replace("/", "-") + '_' + raw[1].replace("/", "-")
    if ext:
        new_name += '.csv'
    return new_name


parsed_files = map(parse_filename, files)
writer = pd.ExcelWriter(f'{INPUT_DIR}/{OUTPUT_FILE}', engine='xlsxwriter')

for filename in parsed_files:
    file_path = Path(f'{INPUT_DIR}/{filename}')

    if os.path.exists(f'{INPUT_DIR}/{filename}'):
        df = pd.read_csv(f'{INPUT_DIR}/{filename}')
        sheet_name = filename[:-4][0:31]
        print(sheet_name)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

writer.close()


