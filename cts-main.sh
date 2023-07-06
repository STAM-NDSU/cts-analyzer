#!/bin/bash
COMMIT_START_DATE="01/01/2023"  COMMIT_END_DATE="02/01/2023" nohup python3 main.py &
COMMIT_START_DATE="01/01/2022"  COMMIT_END_DATE="01/01/2023" nohup python3 main.py &

# Traversing fails for a year date range in 2021; break down into multiple time periods
COMMIT_START_DATE="09/29/2021"  COMMIT_END_DATE="01/01/2022" nohup python3 main.py &
COMMIT_START_DATE="07/30/2021"  COMMIT_END_DATE="09/28/2021" nohup python3 main.py &
COMMIT_START_DATE="01/01/2021"  COMMIT_END_DATE="07/29/2021" nohup python3 main.py &

COMMIT_START_DATE="01/01/2020"  COMMIT_END_DATE="01/01/2021" nohup python3 main.py &
COMMIT_START_DATE="01/01/2019"  COMMIT_END_DATE="01/01/2020" nohup python3 main.py &
COMMIT_START_DATE="01/01/2018"  COMMIT_END_DATE="01/01/2019" nohup python3 main.py &
COMMIT_START_DATE="01/01/2017"  COMMIT_END_DATE="01/01/2018" nohup python3 main.py &
COMMIT_START_DATE="01/01/2016"  COMMIT_END_DATE="01/01/2017" nohup python3 main.py &
COMMIT_START_DATE="01/01/2015"  COMMIT_END_DATE="01/01/2016" nohup python3 main.py &
COMMIT_START_DATE="01/01/2014"  COMMIT_END_DATE="01/01/2015" nohup python3 main.py &
COMMIT_START_DATE="01/01/2013"  COMMIT_END_DATE="01/01/2014" nohup python3 main.py &
COMMIT_START_DATE="01/01/2012"  COMMIT_END_DATE="01/01/2013" nohup python3 main.py &
COMMIT_START_DATE="01/01/2011"  COMMIT_END_DATE="01/01/2012" nohup python3 main.py &
COMMIT_START_DATE="01/01/2010"  COMMIT_END_DATE="01/01/2011" nohup python3 main.py &
COMMIT_START_DATE="01/01/2009"  COMMIT_END_DATE="01/01/2010" nohup python3 main.py &
