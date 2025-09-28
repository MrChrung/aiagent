import os
import subprocess
import sys

from google import genai
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, optionally with arguments, within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.TYPE_UNSPECIFIED,
                description="A python list of arguments to add to the command",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    working_path = os.path.abspath(working_directory)
    full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not (full_file_path.startswith(working_path)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not (os.path.exists(full_file_path)):
        return f'Error: File "{file_path}" not found.'
    if not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        arguments = [sys.executable, full_file_path] + list(args or [])
        process = subprocess.run(arguments,timeout=30, text=True, cwd=working_path, capture_output=True)
        # print("DEBUG ++++++++++++++++++++")
        # print(process)
        # print(working_path)
        # print(full_file_path)
        # print("DEBUG --------------------")

        result = ""
        output_str = f"STDOUT: {process.stdout}"
        error_str = f"STDERR: {process.stderr}"
        result += output_str + "\n" + error_str + "\n"
        if process.check_returncode:
            result += f"Process exited with code {process.returncode}"
        return result or "No output produced"
    except Exception as e:
        print(f"Error: executing Python file: {e}")
        pass