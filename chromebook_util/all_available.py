import os
from check_chromebook import check, get_info
folder_name = 'chromebook_data'

"""
Function that returns a list of the data of all chromebook bin ids available at an inputted date and period.
Args:
    date (string)
    period (string)
Returns:
    (list of lists)
    Example: [['A2', 'math hall', '8'], ['A32', 'Gibsonland', '6']]
"""
def available_chromebooks(date, period):
    available = []
    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)):
            if check(id, date, period):
                available.append(get_info(id))
    return available

# # sample test
# print(available_chromebooks('2024-12-31', '2'))