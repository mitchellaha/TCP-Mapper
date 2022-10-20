import os
import errno
import json


def get_file_type(FileName):
    """
    Returns the File Type if TCP or PDF
    """
    if FileName.lower().endswith('.tcp'):  # ? Could Probably Use os.path.splitext('my_file.pdf')[1] to get the file type
        return "tcp"
    elif FileName.lower().endswith('.pdf'):  # ? Could Probably Use os.path.splitext('my_file.pdf')[1] to get the file type
        return "pdf"
    else:
        return "other"


def get_files_from_directory(Directory):
    """
    Returns a list of all the files in the directory and subdirectories.
    
    params
    ------
    Directory: string
        Path to the directory
        
    returns
    -------
    fileList: list
        List of all the files in the directory
    """
    allFileNames = []
    for subdir, dirs, files in os.walk(Directory):
        print("Walking: " + str(subdir))
        for file in files:
            allFileNames.append(os.path.join(subdir, file))
    return allFileNames


def save_to_JSON(Dictionary: dict, FileName: str):  # ? Unused in Main
    """
    Saves the dictionary to a JSON file in the /output/ directory
    """
    # make directory if it doesn't exist
    if not os.path.exists("output"):
        try:
            os.makedirs("output")
        except OSError as exc:  # Guard against
            if exc.errno != errno.EEXIST:
                raise
    with open("./output/" + FileName, "w") as f:
        json.dump(Dictionary, f)
        f.close()
