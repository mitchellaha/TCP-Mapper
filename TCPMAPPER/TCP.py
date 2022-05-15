import os
import json
from datetime import datetime as dt
import re


def getFileType(fileName):  # ! Overall Useless Function > Consider Deletion
    """
    Returns the File Type if TCP, TCT, or PDF
    """
    if fileName.lower().endswith('.tcp'):
        return "TCP"
    elif fileName.lower().endswith('.tct'):
        return "TCT"
    elif fileName.lower().endswith('.pdf'):
        return "PDF"
    else:
        return "UNKNOWN"


def firstLine(fullLocation):
    """
    Opens the TCP File and Returns the First Text Line of the TCP File
    """
    with open(fullLocation, "r", errors="ignore", encoding="utf-8") as tcp:
        first_line = tcp.readline()
    return first_line


def findJsonRegex(string):
    """
    Finds the JSON String in the TCP File and returns the JSON String
    """
    jsonString = re.findall(r'{.*}', string)
    if len(jsonString) > 1:
        print("findJsonRegex: Error Found Multiple for: \n" + string)
    return json.loads(jsonString[0])


# split the comments by line into a dictionary
def comments(comments):
    """
    Split the Line Breaks in the Comments and return a Dictionary of the Comments
    """
    commentDict = {}
    if comments is not None:
        for i, line in enumerate(comments.splitlines()):
            if i == 0:
                commentDict["Customer"] = line
            elif i == 1:
                commentDict["AddressOne"] = line
            elif i == 2:
                commentDict["AddressTwo"] = line
            elif i == 3:
                commentDict["Contact"] = line
            elif i == 4:
                commentDict["JobPO"] = line
    return commentDict


class TCPInfoObject(object):
    def __init__(self, RawTcpDict):
        """
        Initialize the TCPInfoObject with the Raw TCP Dictionary
        """
        for key in RawTcpDict.keys():
            # ? For Every Key/Value Pair That isnt Properties add it to the TCPInfoObject
            if key != "Properties":
                setattr(self, key, RawTcpDict[key])
            else:
                for propertiesKey in RawTcpDict[key].keys():
                    # ? Converts "null" or "" Values to None
                    if RawTcpDict[key][propertiesKey] == "null" or RawTcpDict[key][propertiesKey] == "":
                        RawTcpDict[key][propertiesKey] = None
                    # ? For Every Key/Value Pair That isnt Comments add to the TCPInfoObject Object
                    if propertiesKey != "Comments":
                        setattr(self, propertiesKey, RawTcpDict[key][propertiesKey])
                    else:
                        # ? Split the Comments by Line and Add to the TCPInfoObject Object
                        formatComments = comments(RawTcpDict[key][propertiesKey])
                        for commentsKey in formatComments.keys():
                            setattr(self, commentsKey, formatComments[commentsKey])
            if RawTcpDict[key] == "null" or RawTcpDict[key] == "":
                RawTcpDict[key] = None

        if self.EditTime:  # ? Converts EditTime to Integer
            self.EditTime = int(self.EditTime)

        if self.CreatedOn:  # ? Converts CreatedOn to Datetime Object
            self.CreatedOn = dt.strptime(
                self.CreatedOn.split(".")[0], "%Y-%m-%dT%H:%M:%S")

        if self.OriginLng and self.OriginLat is not None:  # ? Converts OriginLng and OriginLat to Decimal
            self.OriginLng = float(self.OriginLng)
            self.OriginLat = float(self.OriginLat)

    def dict(self):
        """
        Returns the Formatted and Flattened Dictionary of the TCPInfoObject Object
        """
        dict = self.__dict__
        # ? Converts the CreatedOn DateTime to a Datetime String
        dict["CreatedOn"] = dict["CreatedOn"].__str__()
        return dict

    def json(self):
        """
        Returns the Formatted JSON For the TCPInfoObject Object
        """
        return json.dumps(self.__dict__)


class TCP:
    def __init__(self, FileLocation):
        """
        Initialize the TCP Object with the File Location
        """
        self.FileLocation = FileLocation
        self.FileName = os.path.basename(FileLocation)
        self.FileDirectory = os.path.dirname(FileLocation)
        self.FileType = getFileType(self.FileLocation)
        self.FirstLine = firstLine(self.FileLocation)
        self.RawInfo = findJsonRegex(self.FirstLine)
        self.info = TCPInfoObject(self.RawInfo)

    def getFileType(self):
        """
        Returns the File Type if TCP or TCT
        """
        return self.FileType

    def getFirstLine(self):
        """
        Returns the First Line of the TCP/TCT File
        """
        return self.FirstLine

    def getRawInfo(self):
        """
        Returns the Raw TCP Dictionary
        """
        return self.RawInfo

    def getTcpDict(self):
        """
        Returns the Formatted TCP Dictionary
        """
        return self.info.dict()

    def getTcpJson(self):
        """
        Returns the Formatted TCP JSON
        """
        return self.info.json()

    def dict(self):
        """
        Returns the Formatted and Flattened Dictionary of the TCP Object with FileInfo
        """
        tcpInfoDict = self.info.dict()
        tcpInfoDict["FileName"] = self.FileName
        tcpInfoDict["FileDirectory"] = self.FileDirectory
        tcpInfoDict["FileType"] = self.FileType
        return self.info.dict()

    def json(self):
        """
        Returns the Formatted JSON For the TCP Object with FileInfo
        """
        return json.dumps(self.dict(), indent=4)

if __name__ == "__main__":
    # ! Test Code
    from pprint import pprint
    tcpFile = "/Users/mitchellaha/Desktop/TCPDemoFile.tcp"
    tcp = TCP(tcpFile)
    pprint(tcp.dict())
    # print(tcp.json())
