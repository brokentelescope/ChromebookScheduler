import os
folder_name = 'chromebook_data'
# function that will take id, date and period as input and true if it is not reserved and false if it is

def check(id, date, period):
    id = os.path.join(folder_name, id)
    with open(id, 'r') as file:
        for line in file:
            if date+','+period in line:
                return 'none' in line
    # if date/period not found, return False
    return False

# # sample test
# print(check('A2', '2024-12-31', 'C'))