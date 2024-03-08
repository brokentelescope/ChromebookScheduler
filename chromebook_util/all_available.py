import os
from check_chromebook import check, get_info
folder_name = 'chromebook_data'

# function that returns a list of all chromebook bin ids at a date/period
def available_chromebooks(date, period):
    available = []
    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)):
            if check(id, date, period):
                available.append(get_info(id))
    return available

print(available_chromebooks('2024-12-31', '2'))