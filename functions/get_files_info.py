import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
def get_files_info(working_directory, directory=","):
    try:
        joined = os.path.join(working_directory, directory)
        dir_path = os.path.abspath(joined)
        working_path = os.path.abspath(working_directory)
    except Exception as e:
        return (f"Error: {e}")
    if not (dir_path.startswith(working_path ) or dir_path == working_directory):
        return (f"'Error: Cannot list '{directory}' as it is outside the permitted working directory'")
    if not os.path.isdir(dir_path):
        return f'Error: "{dir_path}" is not a directory'
    
    try:
        dir_names = os.listdir(dir_path)
        res = ""
        for f in dir_names:
                path = os.path.join(dir_path, f)
                size = os.path.getsize(path)
                is_dir = not os.path.isfile(path)
                res += f"- {f}: file_size={size} bytes, is_dir={is_dir}\n"
    except Exception as e:
        return f"Error: {e}"
    return res

