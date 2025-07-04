import os

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir
    if directory:
        target_dir = os.path.abspath(os.path.join(abs_working_dir,directory))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        files_list = []
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            file_size = 0
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            file_info = f'{file_name}: file_size={file_size} bytes, is_dir={is_dir}'
            files_list.append(file_info)
        return  "\n".join(files_list)
    except Exception as e:
        return f'Error: {e}'
