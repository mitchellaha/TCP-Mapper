import os

from handlers.metadata_handler import get_file_metadata
from handlers.mongodb_handler import FILE_Mongo
from handlers.tcp_handler import TCP
from utils.datetime_utils import metadata_dt_convert
from utils.file_utils import get_files_from_directory, get_file_type

PDF_MONGO = FILE_Mongo("pdf")  # ? Not sure if I Should make this a constant or not...
TCP_MONGO = FILE_Mongo("tcp")  # ? Not sure if I Should make this a constant or not...

def file_runner(FilePath):
    """
    Returns a dictionary of the file's metadata and information if plan.
    
    params
    ------
    filePath: string
        Path to the file

    returns
    -------
    dict: dictionary
        Dictionary of the file's metadata and information
    """
    fileType = get_file_type(FilePath)
    fileMetaData = metadata_dt_convert(get_file_metadata(FilePath))

    if fileType == "pdf":
        return fileMetaData
    elif fileType == "tcp":
        tcpInfo = TCP(FilePath).infoDict()
        return {**fileMetaData, **tcpInfo}


def process_single_file(FilePath, Update=False):
    """
    Processes a single file and inserts it into the database if PDF or TCP.
    
    params
    ------
    FilePath: string
        Path to the file to be processed and inserted into the database.
    """
    fileType = get_file_type(FilePath)
    if fileType == "pdf":
        if PDF_MONGO.check_if_exists(Path=FilePath):
            print("File already exists in the database: " + str(FilePath))
            if Update:
                print("...Updating file")
                PDF_MONGO.update_one(file_runner(FilePath))
        else:
            PDF_MONGO.insert_one(file_runner(FilePath))
    elif fileType == "tcp":
        if TCP_MONGO.check_if_exists(Path=FilePath):
            print("File already exists in the database: " + str(FilePath))
            if Update:
                print("...Updating file")
                TCP_MONGO.update_one(file_runner(FilePath))
        else:
            TCP_MONGO.insert_one(file_runner(FilePath))
    else:
        print("Not a PDF or TCP: " + str(FilePath))


def update_single_file(FilePath):
    """
    Updates a single file in the database if it is already in the database.
    
    params
    ------
    FilePath: string
        Path to the file to be analyzed
        
    returns
    -------
    None
    """
    fileType = get_file_type(FilePath)

    if fileType == "pdf":
        if PDF_MONGO.check_if_exists(Path=FilePath):
            PDF_MONGO.update_one(file_runner(FilePath))
        else:
            print("File not in the database: " + str(FilePath))
            print("Consider running process_single_file()")

    elif fileType == "tcp":
        if TCP_MONGO.check_if_exists(Path=FilePath):
            TCP_MONGO.update_one(file_runner(FilePath))
        else:
            print("File not in the database: " + str(FilePath))
            print("Consider running process_single_file()")

    else:
        print("Not a PDF or TCP: " + str(FilePath))


def process_file_list(FileList, Update=False):
    """
    Processes a list of files and inserts them into the database if PDF or TCP.

    - Removes files from list if they already exist in the database.
    
    params
    ------
    FileList: list
        List of files WITH FULL PATH to be processed and inserted into the database.
    """
    pdfList = []
    tcpList = []
    for file in FileList:
        fileType = get_file_type(file)

        if fileType == "pdf":
            if PDF_MONGO.check_if_exists(Path=file):
                print("File already exists in the database: " + str(file))
                if Update:
                    print("...Updating file")
                    PDF_MONGO.update_one(file_runner(file))
                pass
            else:
                pdfList.append(file_runner(file))

        elif fileType == "tcp":
            if TCP_MONGO.check_if_exists(Path=file):
                print("File already exists in the database: " + str(file))
                if Update:
                    print("...Updating file")
                    PDF_MONGO.update_one(file_runner(file))
                pass
            else:
                tcpList.append(file_runner(file))

        else:
            print("Not a PDF or TCP: " + str(file))

    if len(pdfList) > 0:
        PDF_MONGO.insert_many(pdfList)
    if len(tcpList) > 0:
        TCP_MONGO.insert_many(tcpList)


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


if __name__ == "__main__":

    newDirectoryList = [
        "Z:\\. 2021 - PDF",
        "Z:\\. 2022 - PDF",
        "Z:\\. 2021 - TCP",
        "Z:\\. 2022 - TCP"
    ]

    oldDirectoryList = [
        "Z:\\~ PDF & PLANS ARCHIVE\\~ 2020 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\~ 2020 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\2019 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\2019 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\2018 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\2018 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\2017 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\2017 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\Project Plans 2018 & 19 2.83gb",
        "Z:\\~ PDF & PLANS ARCHIVE\\Project Plans 2017"
    ]
