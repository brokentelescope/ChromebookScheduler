import os
folder_name = 'chromebook_data'

"""
Function that returns the id, location, and chromebook count of a certain bin
Args:
    id (string)
Returns:
    (list of strings)
    Example: get_info('A2') --> ['A2', 'math hall', '8']
"""
def get_info(id):
    new_id = os.path.join(folder_name, id)
    with open(new_id, 'r') as file:
        return [id]+ file.readline().strip().split(',')
    
# sample test
# print(get_info('A2')) 