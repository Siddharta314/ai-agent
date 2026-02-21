from functions import get_file_info, run_python_file, write_file, get_file_content
from google.genai import types

def call_function(function_call, verbose=False):
    function_map = {
        "get_file_content": get_file_content,
        "Write_file": write_file,
        "run_python_file": run_python_file,
        "get_file_info": get_file_info
    }

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    function_name = function_call.name or ""

    try:
        function_to_call = function_map.get(function_name)
        if not function_to_call or not callable(function_to_call):
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
        result = function_to_call(**function_call.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error calling function {function_name}: {e}"},
                )
            ],
        )