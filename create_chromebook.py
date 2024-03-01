import datetime

# function that creates a textfile with the file name as
# the chromebook id, file contents are a list of dates that its available

periods = ['A', 'B', 'C', 'D']
def create(id, year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    with open(id, 'w') as file:
        while start_date <= end_date:
            # print(type(current_date))
            for period in periods:
                file.write(start_date.strftime('%Y-%m-%d') + ',' + period + ',' + 'none' + '\n')
            start_date += delta

# Example usage
year = 2024
create('A2', year)
