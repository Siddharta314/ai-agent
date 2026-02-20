import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_info import schema_get_file_info
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


All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


available_functions = types.Tool(
    function_declarations=[
        schema_get_file_info,
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
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=messages,
        config=config
    )

    if response is None or response.usage_metadata is None:
        return
    if (args.verbose):
        print(f"User prompt: \n{args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"{response.text}")
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")




if __name__ == "__main__":
    main()
