import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, target_file]) != working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not os.path.splitext(target_file)[1] == (".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
        command.extend(args)
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory, timeout=30)
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if result.stdout:
            output_parts.append(f"STDOUT: {result.stdout.strip()}")

        if result.stderr:
            output_parts.append(f"STDERR: {result.stderr.strip()}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")

        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
