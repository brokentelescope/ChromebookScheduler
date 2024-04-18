from datetime import datetime, timedelta
import calendar

def add_next_month_date_and_remove_oldest(file_path):
    # Read all lines from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Remove the first 4 lines (assuming 4 periods per day) to delete the oldest day
    del lines[0:4]

    # Determine the next day to add by parsing the last line's date
    last_line = lines[-1]  # Get the new last line after deletion
    last_date_str = last_line.split(',')[0]
    last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    next_day = last_date + timedelta(days=1)

    # Append the next day's data
    for period in range(1, 5):  # Assuming 4 periods per day
        lines.append(f'{next_day.strftime("%Y-%m-%d")},{period},none\n')

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Adjust the file_path to match the location of your file
add_next_month_date_and_remove_oldest('/ChromebookScheduler/CHROMEBOOKSCHEDULER3/chromebook_data/A2')
add_next_month_date_and_remove_oldest('/ChromebookScheduler/CHROMEBOOKSCHEDULER3/chromebook_data/A32')
add_next_month_date_and_remove_oldest('/ChromebookScheduler/CHROMEBOOKSCHEDULER3/chromebook_data/B3')
add_next_month_date_and_remove_oldest('/ChromebookScheduler/CHROMEBOOKSCHEDULER3/chromebook_data/C4')