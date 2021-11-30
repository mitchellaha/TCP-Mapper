import json
import re
import logging
import os

logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format='%(asctime)s :  %(message)s')

class tcpCheck:
    """
    Takes The Full Location of the TCP file and Returns JSON or Dictionary.

    This Class Simply Receives the Full Location of the TCP File and Returns the JSON String or Dictionary.
    Runs Regex Test to Extract JSON String from First Line of TCP File.
    Runs JSON Decode to Test for Decode Errors.

    Parameters
    ----------
    full location : str
        The Full Location of the TCP File.

    Returns
    -------
    class.json() : str
        The JSON String of the TCP File.

    class.dict() : dict
        A Dictionary of the TCP File JSON String

    See Also
    --------
    tcpFormatter : Takes the tcpCheck().dict() and ReFormats it.

    geoJsonFormatter : Takes the tcpFormatter().dict() and Reformats it for GEOjson.

    Examples
    --------
    >>> tcpDict = tcpCheck("Root\\SubDir\\Fake Rapidplan TCP File.tcp")

    >>> tcpDict.dict()

    {
        "AppName": "RapidPlan",
        "AppVersion": "3.7.18.54",
        "ContentType": 1,
        "Properties": {
            "Title": "",
            "Author": "Mitch A",
            "Comments": "Alnt. Customer\r\n23 Pre Center Pkwy\r\nDenver, CO 80223\r\nFirstName LastName 303-555-4425\r\nDemo PO Numb",
            "OriginLat": "38.9531902592142",
            "OriginLng": "-105.780682734018",
            "Scale": "600",
            "JobStarts": "null",
            "JobEnds": "null",
            "CreatedOn": "2021-09-27T22:08:00.1568760Z",
            "EditTime": "3434"
        }
    }

    """
    def __init__(self, fullLocation: str):
        self.fullLocation = fullLocation

    def firstLine(self):
        """
        Opens the TCP File and Returns the First Text Line of the TCP File
        """
        with open(self.fullLocation, "r", errors="ignore", encoding="utf-8") as tcp:
            first_line = tcp.readline()
        return first_line

    def json(self):
        """
        Runs the Regex Test on the First Line of the TCP File
        IF the Regex Test Fails for Some Reason, will return False and Log the Error.
        """
        regexTest = re.search(r"\{.*\:\{.*\:.*\}\}", self.firstLine())
        reTest = regexTest.group(0)
        if regexTest:
            return reTest
        else:
            logging.warning("Regex Test Failed For File String : %s", self.firstLine())
            return reTest

    def dict(self):
        """
        Tests The Provided JSON String For Decode Errors.
        If Decode Errors Are Found, The JSON String Is Stripped of the first 4 characters
        and an error is logged.
        """
        try:
            goodLoad = json.loads(self.json(), strict=False)
            return goodLoad
        except json.decoder.JSONDecodeError:
            stripfour = self.regexTest[4:]
            issueLoad = json.loads(stripfour, strict=False)
            logging.warning("JSON Decode Issue Warning For File JSON : %s", self.json())
            return issueLoad


if __name__ == "__main__":
    """
    Test Code For tcpCheck Class
    """
    from common import isFileTCP
    rootdir = input('Enter the directory to process: ')
    for subdir, dirs, files in os.walk(rootdir):
        for tcpFile in files:
            fullLocation = os.path.join(subdir, tcpFile)
            print(fullLocation)
            tcpTest = isFileTCP(fullLocation)
            if tcpTest is True:
                testTCP = tcpCheck(fullLocation)
        
                print("\n\n Full Location: ")
                print(testTCP)

                print("\n\n First Line: ")
                print(testTCP.firstLine)

                print("\n\n Dict: ")
                print(testTCP.dict)

                print("\n\n JSON: ")
                print(testTCP.json)
