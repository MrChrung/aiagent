import os
from config import MAX_CHARS
from google import genai
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads up to 10000 characters from a file inside of the working directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
    except Exception as e:
        return "Error: " + e

    if not (full_path.startswith(working_path)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        res = ""
        with open(full_path) as f:
            res = f.read(10000)
            if f.read(1) != "":
                res += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return "Error: " + e
    return res