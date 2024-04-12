import os
folder_name = 'chromebook_data'
# function will take a chromebook id, date, period and reserver_name as input and change the assosciated data value
# if we want to cancel a reservation, set reserver_name to 'none'

def cancel(id, date, period): 
    id = os.path.join(folder_name, id)

    with open(id, 'r') as file:
        lines = file.readlines()

    with open(id, 'w') as file:
        for line in lines:
            line = line.strip()
            print(line)
            if date+','+period in line:
                file.write(date+','+period+','+"none"+'\n')
            else:
                file.write(line+'\n')

# # sample test
# edit('A2', '2024-12-31', 'C', 'Gibson')


