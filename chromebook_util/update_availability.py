"""
Update availability function
ICS4U-03
Owen, Rex, Steven
History: 
Apr 18, 2024: Progam creation
"""
from datetime import datetime, timedelta
import os

def add_next_month_date_and_remove_oldest(file_path):
    """
    Function that deletes the oldest day and adds the the next date into each chromebook data file.
    Args:
        file_path (string)
    Returns:
        none
    """
    # Read all lines from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Remove lines 2-5 (assuming 4 periods per day) to delete the oldest day 
    # skip the first line since that one contains the bin data, location, amount
    del lines[1:5]

    # Determine the next day to add by parsing the last line's date
    last_line = lines[-1]  # Get the new last line after deletion
    last_date_str = last_line.split(',')[0]
    last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    next_day = last_date + timedelta(days=1)

    # Append the next day's data
    for period in range(1, 5):
        lines.append(f'{next_day.strftime("%Y-%m-%d")},{period},none\n')

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def execute():
    # Adjust the file_path to match the location of your file
    folder_name = 'chromebook_data'
    for id in os.listdir(folder_name):
        filename = os.path.join(folder_name, id)
        if os.path.isfile(os.path.join(folder_name, id)):
            add_next_month_date_and_remove_oldest(filename)