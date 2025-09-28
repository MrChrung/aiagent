import os
from google import genai
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory. Creates a file if the file does not already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file at file_path.",
            ),
        },
    ),
)
def write_file(working_directory,  file_path, content):
    working_path = os.path.abspath(working_directory)
    full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    dir_name = os.path.dirname(full_file_path)
    # print("DEBUG ++++++++++++++++++++")
    # print(dir_name)
    # print(working_path)
    # print(full_file_path)
    # print("DEBUG --------------------")
    if not (full_file_path.startswith(working_path)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not (os.path.exists(dir_name)):
        if(len(dir_name) > 0):
            os.makedirs(dir_name)
    try:
        written = 0
        with open(full_file_path, "w") as f:
            written = f.write(content)
        return f'Successfully wrote to "{file_path}" ({written} characters written)'

    except Exception as e:
        return f"Error: {e}"