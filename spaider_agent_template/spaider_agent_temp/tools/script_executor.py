"""
   This module provides functionality to execute batch scripts and system commands.
"""

import subprocess
import platform

def run_batch_script(script: str) -> str:
    """
    Run a batch script on Windows.

    Args:
        script: The batch script to run

    Returns:
        str: The output of the script
    """
    try:
        result = subprocess.run(["cmd.exe", "/c", script], check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as err:
        return f"Error occurred: {str(err)}\nStderr: {err.stderr}"

def run_bash_script(script: str) -> str:
    """
    Run a bash script on Unix-like systems.

    Args:
        script: The bash script to run

    Returns:
        str: The output of the script
    """
    try:
        result = subprocess.run(["/bin/bash", "-c", script], check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as err:
        return f"Error occurred: {str(err)}\nStderr: {err.stderr}"

def run_script(script: str) -> str:
    """
    Run a script using the appropriate method based on the operating system.

    Args:
        script: The script to run

    Returns:
        str: The output of the script
    """
    if platform.system() == "Windows":
        return run_batch_script(script)
    else:
        return run_bash_script(script)

# class RunBatchScriptArgsSchema(BaseModel):
#     script: str

# run_batch_script_tool = Tool.from_function(
#     name="run_batch_script",
#     description="Run a batch script in the integrated terminal.",
#     func=run_batch_script,
#     args_schema=RunBatchScriptArgsSchema
# )

# format = {
#     "type": "function",
#     "function": {
#         "name": "run_batch_script",
#         "description": "Run a batch script in the integrated terminal.",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "script": {
#                             "type": "string",
#                             "description": "The batch script to run"
#             }
#         }
#     },
#         "required": ["script"]
#     }
# }
