import os
from html_generator import code_to_html
PROYECT_FOLDER = 'gurux_small'
# exclude containg the following in path name
EXCLUDE_LIST = ['.git']
temp_folder = 'tmp'

def is_excluded(exclude_list,path):
    for exclude in exclude_list:
        if exclude in path:
            return True
    return False


for root, subdirs, files in os.walk(PROYECT_FOLDER): 
    for file in files:
        file_path = os.path.join(root,file)
        if is_excluded(EXCLUDE_LIST,file_path):
            continue
        print(file_path)
        output_html = os.path.join(temp_folder, file_path+".html")
        print(output_html)
        # TODO: create parent folders if neccesary
        #code_to_html(file_path,output_html)

         
