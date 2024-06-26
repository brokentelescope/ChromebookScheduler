"""
Get info function
ICS4U-03
Owen, Rex, Steven
History: 
Apr 22, 2024: Progam creation
"""
import os
folder_name = os.path.join('data', 'chromebook_data')

def get_info(id):
    """
    Function that returns the id, location, and chromebook count of a certain bin
    Args:
        id (string)
    Returns:
        (list of strings)
        Example: get_info('A2') --> ['A2', 'math hall', '8']
    """
    new_id = os.path.join(folder_name, id)
    with open(new_id, 'r') as file:
        return [id]+ file.readline().strip().split(',')
    
# sample test
# print(get_info('A2')) 