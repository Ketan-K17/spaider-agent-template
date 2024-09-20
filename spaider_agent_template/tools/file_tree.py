from langchain.tools import Tool
from pydantic.v1 import BaseModel
import subprocess


def get_file_tree(directory: str) -> str:
    """
    Returns the file structure of the file system

    args:
        directory: str

    returns:
        str: The file structure of the file system
    """
    try:
        result = subprocess.run(
            f"tree {directory} /F",
            shell=True,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as err:
        return f"Error occurred: {str(err)}"


# class GetFileTreeArgsSchema(BaseModel):
#     directory: str


# get_file_tree_tool = Tool.from_function(
#     name = "get_file_tree",
#     description="Returns the file structure of the file system",
#     func = get_file_tree,
#     args_schema=GetFileTreeArgsSchema
# )
