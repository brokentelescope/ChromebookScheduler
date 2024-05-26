"""
Available chromebooks function
ICS4U-03
Owen, Rex, Steven
History: 
Mar 8, 2024: Progam creation
"""
import os
import check_chromebook
import get_info
folder_name = os.path.join('data', 'chromebook_data')

def available_chromebooks(date, period):
    """
    Function that returns a list of the data of all chromebook bin ids available at an inputted date and period.
    Args:
        date (string)
        period (string)
    Returns:
        (list of lists)
        Example: [['A2', 'math hall', '8'], ['A32', 'Gibsonland', '6']]
    """
    available = []
    for id in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, id)):
            if check_chromebook.check(id, date, period):
                available.append(get_info.get_info(id))
    return available

# # sample test
# print(available_chromebooks('2024-12-31', '2'))