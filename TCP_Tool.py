from app import get_files_from_directory, process_file_list
import json

def process_from_directory(RootDirectory):
    """
    Processes all files in a directory and its subdirectories then inserts them into the database if PDF or TCP.

    params
    ------
    rootDirectory: string
        Path to the root directory of the files to be processed and inserted into the database.
    """
    allFilesList = get_files_from_directory(RootDirectory)
    process_file_list(allFilesList)


with open("./Directories_To_Run.json", "r") as f:
    dirList = json.load(f)


for dir in dirList:
    process_from_directory(dir)
