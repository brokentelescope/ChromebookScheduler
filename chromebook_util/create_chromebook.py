import datetime
import os
folder_name = 'chromebook_data'
periods = 'ABCD'
# function that creates a textfile with the chromebook id as the file name
# data in the form of: date,period,reserved_by
def create(id, year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)

    id = os.path.join(folder_name, id)
    print(id)

    with open(id, 'w') as file:
        while start_date <= end_date:
            for period in periods:
                file.write(start_date.strftime('%Y-%m-%d') + ',' + period + ',' + 'none' + '\n')
            start_date += delta

# # sample test
# year = 2024
# create('A2', year)
