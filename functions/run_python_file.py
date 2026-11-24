import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs/executes a python file/script/.py. Which accepts optional arguments and returns a string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to run or execute",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Additional positional arguments"
                },
            },
            "required": ["file_path"],
        },
    },
}
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #LLM safeguard
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        #catch invalid filepath
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        #catch invalid file extention
        if not absolute_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        #command
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        com_pro = subprocess.run(command, capture_output=True, cwd=working_dir_abs, timeout=30, text=True)

        #output string
        output_string = ""
        if com_pro.returncode != 0:
            output_string += f"Process exited with code {com_pro.returncode}\n"

        if com_pro.stdout == "" and com_pro.stderr == "":
            output_string += "No output produced"
        if com_pro.stdout != "":
            output_string += f"STDOUT: {com_pro.stdout}\n"
        if com_pro.stderr != "":
            output_string += f"STDERR: {com_pro.stderr}"
        return output_string

    except Exception as e:
        return f"Error: {e}"
