import os
from pathlib import Path

import win32com.client  # ! Hell


def get_directory_metadata(rdirectory):  # ! Overall Useless If the Single File Version Exists. Move to Gist and Delete?
    path = Path(rdirectory)
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(str(path))

    colnum, columns = 0, []
    while True:  # ? Gets all metadata columns
        colname = ns.GetDetailsOf(None, colnum)
        if not colname:
            break
        columns.append(colname)
        colnum += 1

    itemList = []
    for item in ns.Items():
        itemDict = {"Path": item.Path}
        itemDict["FileSize"] = os.path.getsize(item.Path)

        for colnum in range(len(columns)):
            colval = ns.GetDetailsOf(item, colnum)
            if colval:
                itemColumn = columns[colnum]
                itemColval = colval
                itemDict[itemColumn] = itemColval
                # print('\t', columns[colnum], colval)  # ? Prints All The Metadata
        itemList.append(itemDict)

    return itemList


def get_file_metadata(rFile):  # ? Should Probably Be Cleaned Up A Bit More
    with Path(rFile) as file:
        sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(str(file.parent))

        colnum, columns = 0, []
        while True:  # ? Gets all metadata columns
            # print("Getting Columns" + str(colnum))
            colname = ns.GetDetailsOf(None, colnum)
            if not colname:
                break
            columns.append(colname)
            colnum += 1

        item = ns.ParseName(str(file.name))
        itemDict = {"Path": item.Path}
        itemDict["FileSize"] = os.path.getsize(rFile)

        for colnum in range(len(columns)):
            # print("Getting Column Values" + str(colnum))
            colval = ns.GetDetailsOf(item, colnum)
            if colval:
                itemColumn = columns[colnum]
                itemColval = colval
                itemDict[itemColumn] = itemColval
                # print('\t', columns[colnum], colval)  # ? Prints All The Metadata

    return itemDict


if __name__ == "__main__":
    from pprint import pprint
    directory = r"C:\Users\MitchAndrews\NotOnedrive\Get_Files_SRC\MonitorRoot"
    saveFileSubDirName = "TestInInLine.json"
    # getAllSubDir(directory, saveFileSubDirName)

    rDirectory = r'Z:\! Auto Index Folder\Regular PDFs & TCPs'
    pprint(get_directory_metadata(rDirectory))

    file = "2022TCP.json"
    rFile = r"C:\Users\MitchAndrews\NotOnedrive\Get_Files_SRC\MainFolders\{}".format(file)
    # pprint(getFileMetaData(rFile))
