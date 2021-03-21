import os
PROYECT_FOLDER = 'gurux'

for root, subdirs, files in os.walk('gurux'):
    for file in files:
        file_path = os.path.join(root,file)
        print(file_path)
