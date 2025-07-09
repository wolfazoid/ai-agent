import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.functions_schema import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    
    if not args:
        print("AI Agent: Gemini 2.0 Flash Model")
        print('Usage: python3 main.py "your prompt here" --verbose')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    generate_content(client, messages, verbose)    
    

def generate_content(client, messages, verbose):
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    When using the function 'get_files_info', you can access the root directory above the working directory.
    """
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


    print(f"Response:\n{response.text}")
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part,verbose=verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Did not receive a function response.")
            if verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "working_directory": './calculator'
    }

    call_args = dict(function_call_part.args)  # make a copy of the args
    call_args['working_directory'] = './calculator'

    function_name = function_call_part.name
    
    if function_name in function_map:
        function_result = function_map[function_name](**call_args)
    else:
        raise Exception("Unknown function name")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    main()
