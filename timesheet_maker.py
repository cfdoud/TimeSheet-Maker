#Python automatics script to record daily timesheets for my work
#Author: Christian Doud: 2024-09-17

import csv
from datetime import datetime, timedelta

#Global variables
#Path to the timesheet file
timesheet_file = "/home/christian/Documents/timesheet.csv"
#Path to the timesheet directory
timesheet_dir = "/home/christian/Documents/"
#Path to the timesheet template
timesheet_template = "/home/christian/Documents/timesheet_template.csv"
#Path to the timesheet backup


def get_week_range():
    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start, end

# 



if __name__ == "__main__":
    start, end = get_week_range()
    print(start, end)