"""
os.path.abspath(): Get an absolute path from a relative path
os.path.join(): Join two paths together safely (handles slashes)
os.path.normpath(): Normalize a path (handles things like ..)
os.path.commonpath(): Get the common sub-path shared by multiple paths
os.listdir(): List the contents of a directory
os.path.isdir(): Check if a path points to an existing directory
os.path.isfile(): Check if a path points to an existing regular file
os.path.getsize(): Get the size of a file (in bytes)
.join(): Join a list of strings together with a given separator
"""
import os
from google.genai import types


schema_get_file_info = types.FunctionDeclaration(
    name="get_file_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_file_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    if os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'
        files_info = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            size = os.path.getsize(item_path)
            files_info.append(f"- {item}: {size} bytes, is_dir={os.path.isdir(item_path)}")
        return "\n".join(files_info)
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
