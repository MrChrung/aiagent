import os
import sys
import config
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

messages=[
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
          ]
system_prompt = config.SYSTEM_PROMPT

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,

    ]
)

def main():
    if len(sys.argv) >= 2:
        print("Hello from aiagent!")
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
                )
        )
        verbose = False
        if len(sys.argv) > 2:
            for arg in sys.argv[2:]:
                match arg:
                    case "--verbose":
                        verbose = True
                        metadata = response.usage_metadata
                        print(f"User prompt: {sys.argv[1]}") 
                        print(f"Prompt tokens: {metadata.prompt_token_count}")
                        print(f"Response tokens: {metadata.candidates_token_count}")
        # Call functions
        if isinstance(response.function_calls, list) and len(response.function_calls) > 0:
            for function_call_part in response.function_calls:
                # print("DEBUG +++++++++++++++++++")
                # print(function_call_part)
                # print(function_call_part.name)
                # print(function_call_part.args)
                # print("DEBUG -------------------")
                function_call_result = call_function(function_call_part, verbose)
                if function_call_result.parts[0].function_response.response:
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception(f"Fatal: no result from {function_call_part.name}")
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        print(response.text)
    else:
        print("error: provide text prompt as argument")
        sys.exit(1)

if __name__ == "__main__":
    main()
