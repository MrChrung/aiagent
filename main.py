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

system_prompt = config.SYSTEM_PROMPT


def main():
    if len(sys.argv) >= 2:
        print("Hello from aiagent!")
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
    # Content to pass into generate_content
        messages=[
            types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
            ]

    # tools/functions for ai to "call"
        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,

            ]
        )
    # System_prompt and functions available to pass into generate_content
        model_configs = types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            tools=[available_functions]
                        )



    # Max number of back-and-forths before a text response is given.
        max_iterations = 20 
        
        # Call generate_content in a loop until response.text is returned, or max_iteration times.
        i = 0
        response_flag = False
        while i < (max_iterations) and response_flag == False:
            functions_left = False
            response_flag = False
            # print(f"I: {i}")
            try:

                
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001", 
                    contents=messages, config = model_configs
                )

                # print(f"DEBUG: {response}")
            # Add candidates to messages/content. candidate.content.parts[0].function_call will contain info abt the function the model wants to call.
                # print("DEBUG +++++++++++")
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if part.function_call:
                            functions_left = True

                        # print(f"PART FUNCTION CALL : {part.function_call}")
                        # print(f"PART FUNCTION TEXT: {part.text}")
                        # print(" ================================= ")
                    messages.append(candidate.content)
                    # print("Candidate +++++++++")
                    # print(candidate.content)
                    # print("Candidate ---------")
                    
                # print("DEBUG -----------")



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
                    # print(f"DEBUG: RESPONSE.FUNCTION_CALLS: {response.function_calls}")
                    for function_call_part in response.function_calls:
                        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                        function_call_result = call_function(function_call_part, verbose)
                        if function_call_result.parts[0].function_response.response:
                            # print(f"DEBUG: FUNCTION_CALL_RESULT.PARTS[0].function_response.response: {function_call_result.parts[0].function_response.response}")
                            # TODO: make sure this is right place for this
                            messages.append(types.Content(role="user", parts=[types.Part(function_response=function_call_result.parts[0].function_response)] ))
                            # print(f"MESSAGES AFTER FUNCTION CALL: {messages}")
                            if verbose:
                                print(f"-> {function_call_result.parts[0].function_response.response}")
                        else:
                            raise Exception(f"Fatal: no result from {function_call_part.name}")
                i += 1
                # print("DEBUG: ===== MESSAGES ====")
                # for message in messages:
                    # print()
                    # print(message)
                    # print(len(message.parts))
                    # print(message.parts[0].function_call)
                    # print(message.parts[0].text)
                    # print()
                if (response.text):
                    # print(f"RESPONSE RECEIVED: {response.text}")
                    #response_flag = True
                    if functions_left == False:
                        print(f"RESPONSE: {response.text}")
                        break
            except Exception as e:
                print(e)
                break
    else:
        print("error: provide text prompt as argument")
        sys.exit(1)

if __name__ == "__main__":
    main()
