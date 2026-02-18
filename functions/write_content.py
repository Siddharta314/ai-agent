import os
def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, target_file]) != working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'