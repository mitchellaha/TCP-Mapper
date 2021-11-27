import json

class geoJsonFormatter:
    """
    Formats TCP Dictionary To GeoJSON.

    This Class Receives a Pre Formatted Dictionary and Formats It For GEOjson Feature Collection.

    Parameters
    ----------
    tcpDict : dict
        A Formatted Dictionary From a TCP file. From tcpFormat()

    fileLocation : str
        Optional File Location.

    Returns
    -------
    geoJsonFormatter : dict
        A Formatted Dictionary for GEOjson.

    See Also
    --------
    tcpCheck : takes a TCP file and extracts the dictionary.
    
    tcpFormatter : takes a TCP file and formats it.

    """
    def __init__(self, tcpDict: dict, fileLocation=None):
        self.type = "Feature"
        self.geometry = self.geometry("Point", [tcpDict["Lng"], tcpDict["Lat"]])
        self.properties = self.properties(tcpDict, fileLocation)

    def geometry(self, geoType: str, geoCoord: list):
        """
        Arguments
        ---------
        geoType : str
            The Type of Geometry.

        geoCoord : list
            The Coordinates of the Geometry.

        Returns
        -------
        geometry : dict
            The Geometry of the Feature.
        """
        return {"type": geoType, "coordinates": geoCoord}

    def properties(self, propDict: dict, FileLocation=None):
        """
        Arguments
        ---------
        propDict : dict
            A Formatted Dictionary From a TCP file. From tcpFormat()

        FileLocation : str
            Optional File Location.

        Returns
        -------
        properties : dict
            The Properties of the Feature.
        """
        geoProperties = {
            "Customer": propDict["Customer"],
            "Author": propDict["Author"],
            "Address": propDict["Address"],
            "Contact": propDict["Contact"],
            "JobPO": propDict["JobPO"],
            "CreatedOn": propDict["CreatedOn"],
            "EditTime": propDict["EditTime"]
        }
        if FileLocation is not None:
            geoProperties["FileLocation"] = FileLocation
        return geoProperties

    def dict(self):
        """
        Returns
        -------
        Dictionary for the specific Class.
        """
        return self.__dict__

    def json(self):
        """
        Returns
        -------
        JSON for the specific Class.
        """
        return json.dumps(self.__dict__)


if __name__ == "__main__":

    demoDict = {
        "Customer": "Fake Customer Name",
        "Address": "Fake Address, 8496 Denver Co",
        "Contact": "ContactISH",
        "JobPO": "PONUMB",
        "Lng": -105.00235,
        "Lat": 39.675063,
        "Author": "Fake Author",
        "CreatedOn": "MM DD YYYY",
        "EditTime": "No Time 4523",
        "Scale": "600",
        "TCPVersion": "These Change So Much"
    }

    demoFileLoc = "\\Fake\\File\\Location.tcp"
    demoFormatted = geoJsonFormatter(tcpDict=demoDict, fileLocation=demoFileLoc)

    print(demoFormatted.dict())
