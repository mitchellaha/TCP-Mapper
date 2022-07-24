import os

from handlers.metadata_handler import get_file_metadata
from handlers.tcp_handler import TCP
from utils.datetime_utils import metadata_dt_convert, tcp_DT_convert
from utils.file_utils import isPDF, isTCP, get_file_names_from_dir, get_file_type
from utils.mongo_utils import insert_list_mongoDB, insert_one_mongoDB, does_file_exist_mongoDB, list_everyone_owner_mongoDB, update_one_mongoDB


def file_runner(FilePath):
    """
    Returns a dictionary of the file's metadata and information if plan.
    
    params
    ------
    filePath: string
        Path to the file

    returns
    -------
    dict[0]: dictionary
        Dictionary of the file's metadata and information
    filetype[1]: string
        Type of file ( pdf or tcp )
    """
    FilePath = os.path.normpath(FilePath)
    filetype = get_file_type(FilePath)

    # if isPDF(FilePath):
    if filetype == "pdf":
        fileMetaData = metadata_dt_convert(get_file_metadata(FilePath))
        return fileMetaData, filetype
    # elif isTCP(FilePath):
    elif filetype == "tcp":
        fileMetaData = metadata_dt_convert(get_file_metadata(FilePath))
        try:
            tcpInfo = tcp_DT_convert(TCP(FilePath).getTcpDict())
        except:  # noqa: E722
            print("TCP Failed: " + str(FilePath))
            tcpInfo = {}
            return fileMetaData, filetype
        return {**fileMetaData, **tcpInfo}, filetype
    else:
        print("Not a PDF or TCP: " + str(FilePath))
        return None, None


def main_from_directory(RootDirectory):
    """
    Main function for the program.  !! DOES NOT CHECK FOR DUPLICATES !!

    params
    ------
    rootDirectory: string
        Path to the root directory of the files to be analyzed

    returns
    -------
    None
    """
    pdfList = []
    tcpList = []
    for subdir, dirs, files in os.walk(RootDirectory):  # ? It may be better to get a list of files first ?
        for file in files:
            print("Starting: " + str(file))

            fileRun = file_runner(os.path.join(subdir, file))  # ? Then Run the file_runner on the list of files ?

            if fileRun[1] == "pdf":  # ? is there a better way to acheive this ?
                pdfList.append(fileRun[0])
            elif fileRun[1] == "tcp":
                tcpList.append(fileRun[0])

    insert_list_mongoDB(pdfList, "pdf")
    insert_list_mongoDB(tcpList, "tcp")


def main_from_file_list(FileList):
    """
    Main function for the program. !! DOES NOT CHECK FOR DUPLICATES !!
    
    params
    ------
    FileList: list
        List of files to be analyzed
        
    returns
    -------
    None
    """
    pdfList = []
    tcpList = []
    for file in FileList:
        normalPath = os.path.normpath(file)
        print("Starting: " + str(normalPath))

        fileRun = file_runner(normalPath)

        if fileRun[1] == "pdf":
            pdfList.append(fileRun[0])
        elif fileRun[1] == "tcp":
            tcpList.append(fileRun[0])

    insert_list_mongoDB(pdfList, "pdf")
    insert_list_mongoDB(tcpList, "tcp")


def main_single_file(FilePath):
    """
    Main function for the program.  !! DOES NOT CHECK FOR DUPLICATES !!
    
    params
    ------
    FilePath: string
        Path to the file to be analyzed
        
    returns
    -------
    None
    """
    print("Starting: " + str(FilePath))
    fileRun = file_runner(os.path.normpath(FilePath))
    if fileRun[1] == "pdf":
        insert_one_mongoDB(fileRun[0], "pdf")
    elif fileRun[1] == "tcp":
        insert_one_mongoDB(fileRun[0], "tcp")
    print("Completed: " + str(FilePath))

def update_single_file(FilePath):
    """
    Main function for the program.
    
    params
    ------
    FilePath: string
        Path to the file to be analyzed
        
    returns
    -------
    None
    """
    print("Starting: " + str(FilePath))
    fileRun = file_runner(os.path.normpath(FilePath))
    if fileRun[1] == "pdf":
        update_one_mongoDB(fileRun[0], "pdf")
    elif fileRun[1] == "tcp":
        update_one_mongoDB(fileRun[0], "tcp")
    print("Completed: " + str(FilePath))


def run_directory(RootDirectory):
    """
    Runs the program from a directory.
    
    params
    ------
    RootDirectory: string
        Path to the root directory of the files to be analyzed
        
    returns
    -------
    None
    """
    allFilesList = get_file_names_from_dir(RootDirectory)
    newFilesList = []
    for file in allFilesList:
        print("Starting: " + str(file))
        if isPDF(file):
            if does_file_exist_mongoDB(file, "pdf") is False:
                print("New PDF: " + str(file))
                newFilesList.append(file)
        elif isTCP(file):
            if does_file_exist_mongoDB(file, "tcp") is False:
                print("New TCP: " + str(file))
                newFilesList.append(file)
        else:
            pass

    print("File Loading Complete..." + str(len(newFilesList)) + " files to be loaded")

    pdfList = []
    tcpList = []
    for file in newFilesList:
        fileRun = file_runner(file)
        if fileRun[1] == "pdf":
            pdfList.append(fileRun[0])
        elif fileRun[1] == "tcp":
            tcpList.append(fileRun[0])

    print("Inserting Files into MongoDB...")
    if len(pdfList) > 0:
        insert_list_mongoDB(pdfList, "pdf")
    if len(tcpList) > 0:
        insert_list_mongoDB(tcpList, "tcp")



if __name__ == "__main__":

    pdfDirectoryList = [
        "Z:\\. 2021 - PDF",
        "Z:\\. 2022 - PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\~ 2020 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\2019 PDF",
    ]
    tcpDirectoryList = [
        "Z:\\. 2021 - TCP",
        "Z:\\. 2022 - TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\~ 2020 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\2019 TCP",
    ]
    modernDirectoryList = pdfDirectoryList + tcpDirectoryList

    oldDirectoryList = [
        "Z:\\~ PDF & PLANS ARCHIVE\\2018 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\2018 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\2017 PDF",
        "Z:\\~ PDF & PLANS ARCHIVE\\2017 TCP",
        "Z:\\~ PDF & PLANS ARCHIVE\\Project Plans 2018 & 19 2.83gb",
        "Z:\\~ PDF & PLANS ARCHIVE\\Project Plans 2017"
    ]


    # for directory in oldDirectoryList:
    #     print("Starting: " + str(directory))
    #     run_directory(directory)

    # everyoneOwnerTCPFiles = list_everyone_owner_mongoDB("tcp")
    # print("Everyone Owner Files: " + str(len(everyoneOwnerTCPFiles)))
    # for file in everyoneOwnerTCPFiles:
    #     print("Starting: " + str(file))
    #     update_single_file(file)

    # everyoneOwnerPDFFiles = list_everyone_owner_mongoDB("pdf")
    # print("Everyone Owner Files: " + str(len(everyoneOwnerPDFFiles)))
    # for file in everyoneOwnerPDFFiles:
    #     update_single_file(file)
