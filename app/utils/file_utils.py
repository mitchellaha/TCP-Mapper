import os


def isTCP(file):
    if file.endswith(".tcp"):
        return True
    else:
        return False

def isPDF(file):
    if file.endswith(".pdf"):
        return True
    else:
        return False

def get_file_type(FileName):  # ! New Untested with FileRunner since written on Darwin system
    """
    Returns the File Type if TCP or PDF
    """
    if FileName.lower().endswith('.tcp'):
        return "tcp"
    elif FileName.lower().endswith('.pdf'):
        return "pdf"
    else:
        return "other"


def get_file_names_from_dir(Directory):
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
        print(subdir)
        for file in files:
            allFileNames.append(os.path.join(subdir, file))
    return allFileNames
