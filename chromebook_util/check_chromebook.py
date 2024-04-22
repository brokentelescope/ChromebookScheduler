import os
folder_name = 'chromebook_data'
"""
Function checks if a chromebook is available at a given period
Args:
    id (string)
    date (string)
    period (string)
Returns:
    (boolean)
"""
def check(id, date, period):
    new_id = os.path.join(folder_name, id)
    with open(new_id, 'r') as file:
        for line in file:
            if date+','+period in line:
                return 'none' in line
    # if date/period not found, return False
    return False

# # sample test
# print(check('A2', '2024-12-31', 'C'))