import os
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .write_file import write_file
from google import genai
from google.genai import types


def call_function(call_function_part, verbose=False):
    func_name = call_function_part.name
    func_args = call_function_part.args
    func_args["working_directory"] = "./calculator"
    if verbose == True:
        print(f"CALL_FUNCTION: Calling function: {func_name}({func_args})")
    else:
        print(f"CALL_FUNCTION: Calling function: {func_name}")
    
    functions = {
        "get_file_content":get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if func_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    else:
        try:
            function_result = functions[func_name](**func_args)
            return types.Content(
                role="tool",
                parts=[ # do this.parts[0].response f0r response etc.
                    types.Part.from_function_response(
                        name=func_name,
                        response={"result": function_result},
                    )
                ],
            )
        except TypeError as e:
            return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=func_name,
                            response={"error": f"Unknown function: {func_name}"},
                        )
                    ],
                )