import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function
from functions.get_file_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

If there are errors or the user asks you to fix something, read the files that content the problem and evaluate and fix the problem with write_file. then you can run the file to check if the problem is fixed.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

MAX_ITERATIONS = 20

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
    ],
)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0,
        tools=[available_functions]
    )
    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=messages,
            config=config
        )

        if getattr(response, "candidates", None):
            for candidate in response.candidates:
                if getattr(candidate, "content", None):
                    messages.append(candidate.content)

        if not response.function_calls:
            print(f"{response.text}")
            return

        function_responses = []
        for call in response.function_calls:
            function_call_result = call_function(call, verbose=args.verbose)
            if hasattr(function_call_result, "parts"):
                function_responses.extend(function_call_result.parts)
            else:
                function_responses.append(function_call_result)

        if response is None or response.usage_metadata is None:
            return
        if function_responses:
            messages.append(types.Content(role="user", parts=function_responses))
        if (args.verbose):
            print(f"User prompt: \n{args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        # Print latest assistant text (may be intermediate)
        print(f"{response.text}")

    # If we exit the loop without returning, we've hit the max iterations.
    print("""Error: reached maximum iterations without a final model response.
        The model still requested function calls.""")
    sys.exit(1)


if __name__ == "__main__":
    main()
