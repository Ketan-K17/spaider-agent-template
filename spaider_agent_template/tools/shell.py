import subprocess
from pydantic.v1 import BaseModel
from langchain.tools import Tool

def run_batch_script(script: str) -> str: 
    """
    Run a batch script in the integrated terminal.

    Args:
        script: The batch script to run

    Returns:
        str: The output of the batch script
    """
    try:
        result = subprocess.run(script, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as err:
        return f"Error occurred: {str(err)}"

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
