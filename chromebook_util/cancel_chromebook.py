import os
folder_name = 'chromebook_data'
"""
Function that will cancel a reservation and make that chromebook available again.
Args:
    id (string)
    date (string)
    period (string)
Returns:
    none
"""
def cancel(id, date, period): 
    id = os.path.join(folder_name, id)

    with open(id, 'r') as file:
        lines = file.readlines()

    with open(id, 'w') as file:
        for line in lines:
            line = line.strip()
            if date+','+period in line:
                # change the name back to none
                # we need to make sure that users cannot make their username none
                file.write(date+','+period+','+"none"+'\n')
            else:
                file.write(line+'\n')

# # sample test
# edit('A2', '2024-12-31', '3')


