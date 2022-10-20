import os
from pathlib import Path

import win32com.client  # ! Hell


def get_file_metadata(rFile) -> dict:  # ? Should Probably Be Cleaned Up A Bit More
    with Path(rFile) as file:
        sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
        ns = sh.NameSpace(str(file.parent))

        colnum, columns = 0, []
        while True:  # ? Gets all metadata columns
            colname = ns.GetDetailsOf(None, colnum)
            if not colname:
                break
            columns.append(colname)
            colnum += 1

        item = ns.ParseName(str(file.name))
        itemDict = {"Path": item.Path}
        itemDict["FileSize"] = os.path.getsize(rFile)

        for colnum in range(len(columns)):  # ? Gets the Values for the Columns
            colval = ns.GetDetailsOf(item, colnum)
            if colval:
                itemColumn = columns[colnum]
                itemColval = colval
                itemDict[itemColumn] = itemColval
                # print('\t', columns[colnum], colval)  # ? Prints All The Metadata

    return itemDict
