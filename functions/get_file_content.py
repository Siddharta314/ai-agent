import os
MAX_CHARS = 10000
def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory, target_file]) == working_directory:
        if os.path.isfile(target_file):
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read(MAX_CHARS)
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return content
        return f'Error: File not found or is not a regular file: "{file_path}"'
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

# f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
# f'Error: File not found or is not a regular file: "{file_path}"'