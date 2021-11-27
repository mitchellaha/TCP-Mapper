import json
from datetime import datetime as dt
from datetime import timedelta as td

class tcpFormatter:
    """
    Formats Extracted Dictionary From TCP File.

    This Class Simply Recives a Dictionary From The TCP File and
    returns it into the prefered formatting.

    Parameters
    ----------
    tcpDict : dict
        A dictionary extracted from a TCP file. (NOT a JSON string)

    latLngFix : bool
        If True then the lat and lng will be checked for 'null' and replaced with wyoming lake.
        If False then the lat and lng will be converted to float.

    Returns
    -------
    class.dict() : dict
        A Formatted dictionary of the TCP File Info.

    class.json() : str
        A JSON formatted string of the above dictionary.

    See Also
    --------
    tcpCheck : takes a TCP file and extracts the dictionary.

    Examples
    --------
    >>> tcpDict = tcpCheck("FULLTCPLOCATION").dict()

    >>> tcpFormat = tcpFormatter(tcpDict)

    >>> print(tcpFormat.dict())
    {
        'Customer': '******',
        'Address': '******',
        'Contact': '******',
        'JobPO': '******',
        'Lng': '******',
        'Lat': '******',
        'Author': '******',
        'CreatedOn': '******',
        'EditTime': '******',
        'Scale': '******',
        'TCPVersion': '******'
    }

    """
    def __init__(self, tcpDict: dict, latLngFix=False):
        self.Customer = self.comments(tcpDict["Properties"]["Comments"])["Customer"]
        self.Address = self.comments(tcpDict["Properties"]["Comments"])["Address"] + ", " + self.comments(tcpDict["Properties"]["Comments"])["Address2"]
        self.Contact = self.comments(tcpDict["Properties"]["Comments"])["Contact"]
        self.JobPO = self.comments(tcpDict["Properties"]["Comments"])["JobPO"]
        self.Lng = self.latlngfix(tcpDict["Properties"], latLngFix=latLngFix)[0]
        self.Lat = self.latlngfix(tcpDict["Properties"], latLngFix=latLngFix)[1]
        self.Author = tcpDict["Properties"]["Author"]
        self.CreatedOn = self.createdDate(tcpDict["Properties"]["CreatedOn"])
        self.EditTime = self.editTime(tcpDict["Properties"]["EditTime"])
        self.Scale = tcpDict["Properties"]["Scale"]
        self.TCPVersion = tcpDict["AppVersion"]
        # self.Title = tcpDict["Properties"]["Title"]
    
    def editTime(self, editTime):
        """
        Takes a TCP time string in seconds and returns a formatted string  HH:MM:SS
        """
        convertType = int(editTime)
        return str(td(seconds=convertType))

    def createdDate(self, createdOn):
        """
        Takes a TCP created date string and returns a formatted string YYYY-MM-DD HH:MM:SS
        """
        fix = dt.strptime(createdOn[:-2], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        return str(fix)

    def jobPO(self, tcpDict):
        """
        Returns the Job PO Number with IF Else Statement to check if the location of the Job PO is in the Comments or Title
        """
        if tcpDict["Properties"]["Title"] == '':
            jobPO = tcpDict["Properties"]["Title"]
        else:
            jobPO = self.comments(tcpDict)["JobPO"]
        return jobPO

    def comments(self, comments):
        """
        Split the Line Breaks in the Comments and return a Dictionary of the Comments
        """
        commentDict = {
            "Customer": "",
            "Address": "",
            "Address2": "",
            "Contact": "",
            "JobPO": ""
        }
        if comments is not None:
            for i, line in enumerate(comments.splitlines()):
                if i == 0:
                    commentDict["Customer"] = line
                elif i == 1:
                    commentDict["Address"] = line
                elif i == 2:
                    commentDict["Address2"] = line
                elif i == 3:
                    commentDict["Contact"] = line
                elif i == 4:
                    commentDict["JobPO"] = line
        return commentDict

    def latlngfix(self, properties, latLngFix=False):
        """
        if latlngFix is True then lat and lng will be checked for 'null' and replaced with wyoming lake else float
        """
        if latLngFix is False:
            return float(properties["OriginLng"]), float(properties["OriginLat"])
        if latLngFix is True:
            if properties["OriginLng"] == "null":
                return float(-108.601), float(43.1834)
            else:
                return float(properties["OriginLng"]), float(properties["OriginLat"])

    def dict(self):
        """
        Returns the Formatted Dictionary For the Provided tcpDict
        """
        return self.__dict__

    def json(self):
        """
        Returns the Formatted JSON For the Provided tcpDict
        """
        return json.dumps(self.__dict__)

if __name__ == "__main__":
    """
    Test Code For tcpFormatter Class
    """

    test = {
        "AppName": "RapidPlan",
        "AppVersion": "3.7.15.47",
        "ContentType": 1,
        "Properties": {
            "Title": "",
            "Author": "Mitch A",
            "Comments": "Alnt. Customer\r\n23 Pre Center Pkwy\r\nDenver, CO 80223\r\nFirstName LastName 303-555-4425\r\nDemo PO Numb",
            "OriginLat": "null",
            "OriginLng": "null",
            "Scale": "600",
            "JobStarts": "null",
            "JobEnds": "null",
            "CreatedOn": "2021-05-05T17:14:04.7141433Z",
            "EditTime": "18272"
        }
    }

    x = tcpFormatter(test)

    print("\n\n Values: ")
    print("TCP Version: " + x.TCPVersion)
    print("Customer: " + x.Customer)
    print("Address: " + x.Address)
    print("Contact: " + x.Contact)
    print("JobPO: " + x.JobPO)
    print(f"Lat: {x.Lat}")
    print(f"Lng: {x.Lng}")
    print("Scale: " + x.Scale)
    print("CreatedOn: " + x.CreatedOn)
    print("EditTime: " + x.EditTime)

    print("\n\n Dict: ")
    print(x.dict())

    print("\n\n JSON: ")
    print(x.json())

    test = {
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

    y = tcpFormatter(test)

    print("\n\n Values: ")
    print("TCP Version: " + y.TCPVersion)
    print("Customer: " + y.Customer)
    print("Address: " + y.Address)
    print("Contact: " + y.Contact)
    print("JobPO: " + y.JobPO)
    print(f"Lat: {y.Lat}")
    print(f"Lng: {y.Lng}")
    print("Scale: " + y.Scale)
    print("CreatedOn: " + y.CreatedOn)
    print("EditTime: " + y.EditTime)

    print("\n\n Dict: ")
    print(y.dict())

    print("\n\n JSON: ")
    print(y.json())
