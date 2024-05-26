import os

folder_name = os.path.join('data', 'chromebook_data')

def edit(id, date, period, reserver_name):
    """
    Function will take a chromebook id, date, period, and reserver_name as input and change the associated data value.
    If we want to cancel a reservation, set reserver_name to 'none'
    Args:
        id (string)
        date (string)
        period (string)
        reserver_name (string) 
    Returns:
        none
    """
    id_path = os.path.join(folder_name, id)

    # Read the existing lines from the file
    with open(id_path, 'r') as file:
        lines = file.readlines()

    # Write the modified lines back to the file
    with open(id_path, 'w') as file:
        for line in lines:
            line = line.strip()
            if date + ',' + period in line:
                file.write(date + ',' + period + ',' + reserver_name + '\n')
            else:
                file.write(line + '\n')

# Sample test
edit('A2', '2024-12-31', 'C', 'Gibson')
