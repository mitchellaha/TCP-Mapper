from app.handlers.metadata_handler import get_file_metadata
from app.handlers.mongodb_handler import FILE_Mongo
from app.handlers.tcp_handler import TCP
from app.utils.datetime_utils import metadata_dt_convert
from app.utils.file_utils import get_file_type

PDF_MONGO = FILE_Mongo("pdf")  # ? Not sure if I Should make this a constant or not...
TCP_MONGO = FILE_Mongo("tcp")  # ? Not sure if I Should make this a constant or not...


def get_file_data(FilePath):
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
    Update: boolean
        If True - Existing Files Shall Be Updated In Database
        If False - Existing Files Will Be Ignored
    """
    fileType = get_file_type(FilePath)
    if fileType == "pdf":
        if PDF_MONGO.check_if_exists(Path=FilePath):
            print("File already exists in the database: " + str(FilePath))
            if Update:
                print("...Updating file")
                PDF_MONGO.update_one(get_file_data(FilePath))
        else:
            PDF_MONGO.insert_one(get_file_data(FilePath))
    elif fileType == "tcp":
        if TCP_MONGO.check_if_exists(Path=FilePath):
            print("File already exists in the database: " + str(FilePath))
            if Update:
                print("...Updating file")
                TCP_MONGO.update_one(get_file_data(FilePath))
        else:
            TCP_MONGO.insert_one(get_file_data(FilePath))
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
    Update: boolean
        If True - Existing Files Shall Be Updated In Database
        If False - Existing Files Will Be Ignored
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
                    PDF_MONGO.update_one(get_file_data(file))
                pass
            else:
                pdfList.append(get_file_data(file))

        elif fileType == "tcp":
            if TCP_MONGO.check_if_exists(Path=file):
                print("File already exists in the database: " + str(file))
                if Update:
                    print("...Updating file")
                    PDF_MONGO.update_one(get_file_data(file))
                pass
            else:
                tcpList.append(get_file_data(file))

        else:
            print("Not a PDF or TCP: " + str(file))

    if len(pdfList) > 0:
        PDF_MONGO.insert_many(pdfList)
    if len(tcpList) > 0:
        TCP_MONGO.insert_many(tcpList)
