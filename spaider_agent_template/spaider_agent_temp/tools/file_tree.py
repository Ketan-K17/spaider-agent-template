from langchain.tools import Tool
from pydantic.v1 import BaseModel
import subprocess
import platform

# def get_file_tree(directory: str) -> str:
#     """
#     Returns the file structure of the file system

#     args:
#         directory: str

#     returns:
#         str: The file structure of the file system
#     """
#     try:
#         result = subprocess.run(
#             f"tree {directory} /F",
#             shell=True,
#             check=True,
#             text=True,
#             capture_output=True,
#         )
#         return result.stdout
#     except subprocess.CalledProcessError as err:
#         return f"Error occurred: {str(err)}"

def get_file_tree(directory: str) -> str:
    """
    Returns the file structure of the file system and the current shell

    args:
        directory: str

    returns:
        str: The file structure of the file system and shell info
    """
    try:
        if platform.system() == "Windows":
            shell_cmd = "echo %COMSPEC%"
            tree_cmd = f"tree {directory} /F"
        else:
            shell_cmd = "echo $SHELL"
            tree_cmd = f"find {directory} -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'"

        shell_info = subprocess.run(shell_cmd, shell=True, check=True, text=True, capture_output=True)
        tree_result = subprocess.run(tree_cmd, shell=True, check=True, text=True, capture_output=True)
        
        return f"Shell: {shell_info.stdout.strip()}\n\nFile Tree:\n{tree_result.stdout}"
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
