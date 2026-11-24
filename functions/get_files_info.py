import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        #LLM safeguard
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        #catch invalid dir
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        #list files
        target_dir_contents: str = f""
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            name: str = item
            file_size: int = os.path.getsize(item_path)
            is_dir: bool = os.path.isdir(item_path)
            target_dir_contents += f"- {name}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return target_dir_contents
    
    except Exception as e:
        return f"Error: {e}"
