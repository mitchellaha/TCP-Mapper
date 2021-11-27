import json
from datetime import datetime as dt
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format='%(asctime)s :  %(message)s')

def isFileTCP(fileName):
    """
    Checks If The File Is A .tcp File.
    """
    try:
        if fileName.lower().endswith('.tcp'):
            return True
        else:
            return False
    except Exception as e:
        logging.error(e)
        return False

def featureCollection(jsonData):
    """
    Packs The GeoJSON Features into a Feature Collection.
    """
    geoJson = {
        "type": "FeatureCollection",
        "features": jsonData
    }
    return geoJson


todaysDate = dt.now().strftime("%Y-%m-%d")

def saveGeoJson(geoJSON):
    """
    Saves The GeoJSON Feature Collection To Two Files
    """
    with open(f'mapdata/{todaysDate}_tcplist.geojson', 'w') as outfile:
        json.dump(geoJSON, outfile)
    with open('mapdata/tcplist.geojson', 'w') as outfile:
        json.dump(geoJSON, outfile)

def saveToJson(dictList):
    """
    Saves The TCP List To a JSON File
    """
    with open(f'mapdata/{todaysDate}_alljson.json', 'w') as outfile:
        json.dump(dictList, outfile)

def saveErrors(issues, issueList, oldFiles, oldFileList):
    """
    Saves The Non TCPs and Non GeoReferenced TCPs To a JSON File
    """
    form = {'Total Non TCPs': issues, 'Non TCP Files': issueList, 'Total Non GeoRef': oldFiles, 'Non GeoRef Files': oldFileList}
    with open(f'mapdata/{todaysDate}_issues.json', 'w') as outfile:
        json.dump(form, outfile)
