import os
folder_name = 'chromebook_data'

def get_info(id):
    new_id = os.path.join(folder_name, id)
    with open(new_id, 'r') as file:
        return [id]+ file.readline().strip().split(',')
    
# # sample test
# print(get_info('A2')) 