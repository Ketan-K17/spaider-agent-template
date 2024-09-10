import subprocess
from pydantic.v1 import BaseModel
from langchain.tools import Tool

def run_batch_script(script):
    try:
        result = subprocess.run(script, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as err:
        return f"Error occurred: {str(err)}"

class RunBatchScriptArgsSchema(BaseModel):
    script: str

run_batch_script_tool = Tool.from_function(
    name="run_batch_script",
    description="Run a batch script in the integrated terminal.",
    func=run_batch_script,
    args_schema=RunBatchScriptArgsSchema
)
