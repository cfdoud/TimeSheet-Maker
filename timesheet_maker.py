import csv
import os
from datetime import datetime, timedelta

# Author: Christian Doud
# Date: 2024-09-17

# Define the directory where timesheets will be saved
TIMESHEET_DIRECTORY = "C:\\Users\\proud\\Documents\\UCI\\Timesheets"

# Function to ensure the timesheet directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

# Function to calculate the start (Monday) and end (Sunday) dates of the current week
def get_week_range():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week, end_of_week

# Function to create the timesheet filename based on the week range
def get_timesheet_filename():
    start_of_week, end_of_week = get_week_range()
    # Format the file name as "timesheet_YYYY-MM-DD_to_YYYY-MM-DD.csv"
    return f'timesheet_{start_of_week.strftime("%Y-%m-%d")}_to_{end_of_week.strftime("%Y-%m-%d")}.csv'

# Function to initialize the weekly timesheet file if it doesn't exist
def initialize_timesheet():
    ensure_directory_exists(TIMESHEET_DIRECTORY)  # Ensure the directory exists
    file_name = os.path.join(TIMESHEET_DIRECTORY, get_timesheet_filename())
    try:
        with open(file_name, 'x', newline='') as file:
            writer = csv.writer(file)
            # Write header row with appropriate columns
            writer.writerow(['Date', 'Task', 'Start Time', 'End Time', 'Total Hours Worked'])
        print(f"Initialized timesheet for the week: {file_name}")
    except FileExistsError:
        print(f"Timesheet for this week already exists: {file_name}")

# Function to convert 12-hour format to 24-hour format
def convert_to_24_hour(time_str):
    # Attempt to parse time in 12-hour format first
    try:
        return datetime.strptime(time_str, "%I:%M%p").strftime("%H:%M")
    except ValueError:
        pass
    
    # If parsing fails, assume it's already in 24-hour format
    return time_str

# Function to calculate the total hours worked between two times
def calculate_hours(start_time, end_time):
    start_time = convert_to_24_hour(start_time)
    end_time = convert_to_24_hour(end_time)
    
    time_format = "%H:%M"  # Expected format: 24-hour HH:MM
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)
    
    # Calculate total hours, handling cases where the end time is past midnight
    total_hours = (end - start).total_seconds() / 3600.0
    if total_hours < 0:
        total_hours += 24
    return total_hours

# Function to record the start and end times for each task
def record_daily_hours():
    file_name = os.path.join(TIMESHEET_DIRECTORY, get_timesheet_filename())
    start_of_week, _ = get_week_range()
    
    for i in range(7):  # Loop through each day of the week
        current_day = start_of_week + timedelta(days=i)
        current_day_str = current_day.strftime('%Y-%m-%d')
        task = input(f"Enter the task for {current_day_str}: ")
        start_time = input(f"Enter the start time for {task} on {current_day_str} (HH:MM, 24-hour format): ")
        end_time = input(f"Enter the end time for {task} on {current_day_str} (HH:MM, 24-hour format): ")

        # Calculate total hours worked for this task
        total_hours = calculate_hours(start_time, end_time)

        # Append the data to the weekly timesheet CSV file
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_day_str, task, start_time, end_time, f'{total_hours:.2f}'])

        print(f"Recorded {total_hours:.2f} hours for task '{task}' on {current_day_str} (from {start_time} to {end_time}).")

# Example usage
if __name__ == "__main__":
    initialize_timesheet()
    record_daily_hours()
