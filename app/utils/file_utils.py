import os


def isTCP(file):  # TODO: Consider Removal
    if file.endswith(".tcp"):
        return True
    else:
        return False

def isPDF(file):  # TODO: Consider Removal
    if file.endswith(".pdf"):
        return True
    else:
        return False

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
