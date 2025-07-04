import os

def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)
    # print(f'Troubleshooting standard functions')
    # print(f'Full Path: {full_path}')
    # print(f'Abs Path: {os.path.abspath(full_path)}')

    if not directory in os.path.abspath(full_path) or not full_path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        f'Error: "{directory}" is not a directory'

    try:
        files_list = []
        for item in os.listdir(full_path):
            file_path = full_path + "/" + item
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            file_info = f'{item}: file_size={file_size} bytes, is_dir={is_dir}'
            files_list.append(file_info)
            
        # dir_contents = list(map(lambda file_name:
        #     full_path + "/" + file_name, os.listdir(full_path)))
        
        # file_info = list(map(lambda file: 
        #     f'{file}: file_size={os.path.getsize(file)} bytes, is_dir={os.path.isdir(file)}', 
        #     dir_contents))
        
    except Exception as e:
        return f'Error: {e}'

    return  "\n".join(files_list)
