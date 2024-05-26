"""
Display two weeks
ICS4U-03
Owen, Rex, Steven 
This is still a work in progress as the client requested it recently.
The code aims to find the corresponding school days 1, 2, 3, 4 for the next two weeks, given a date.
History:
April 3, 2024: Program creation
"""

from datetime import datetime, timedelta

# Get the current date
current_date = datetime.now().date()

# Calculate the next two weeks
for i in range(14):  # for each day in the next two weeks
    next_date = current_date + timedelta(days=i)
    
    # Check if it's a weekday (Monday to Friday)
    if next_date.weekday() < 5:  # 0: Monday, 1: Tuesday, ..., 4: Friday
        print(next_date.strftime("%A, %Y-%m-%d"))
