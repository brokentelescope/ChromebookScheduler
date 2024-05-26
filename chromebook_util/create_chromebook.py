"""
Create chromebooks function
ICS4U-03
Owen, Rex, Steven
History: 
Mar 4, 2024: Progam creation
"""
import datetime
import os
folder_name = os.path.join('data', 'chromebook_data') 
periods = '1234'

def create(id, year, location, amount):
    """
    Function that creates a textfile with the chromebook id as the file name.
    Args:
        id (string)
        year (string)
        location (string)
        amount (string)
    Returns:
        none
        the data is stored in text-files in the format date,period,reserved_by
    """
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    
    id = os.path.join(folder_name, id)

    with open(id, 'w') as file:  # Use 'w' mode instead of 'r'
        file.write(location + ',' + str(amount) + '\n')
        while start_date <= end_date:
            for period in periods:
                file.write(start_date.strftime('%Y-%m-%d') + ',' + period + ',' + 'none' + '\n')
            start_date += delta

