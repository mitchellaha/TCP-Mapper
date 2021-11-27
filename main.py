import logging
import os

from src.common import (featureCollection, isFileTCP, saveErrors, saveGeoJson,
                    saveToJson)
from src.geoJsonFormatter import geoJsonFormatter
from src.programTitle import programTitle
from src.tcpCheck import tcpCheck
from src.tcpFormatter import tcpFormatter

# Create a folder named MapData if it doesnt exist already
try:
    os.mkdir(os.path.join(os.getcwd(), "MapData"))
except FileExistsError:
    pass

# Logging setup
logging.FileHandler(filename='MapData\\TCPMapperLog.log', mode='a')
logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format='%(asctime)s :  %(message)s')

# Print the Logging data to the console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

print(programTitle)
rootdir = input('Enter the directory to process: ')

"""
List Of All TCP Files
"""
tcpList = []
tcpTotal = 0

"""
List Of All NON TCP Files
"""
nonTCPList = []
nonTCPTotal = 0

"""
List Of All Non Geo Referenced Files
"""
nonGeoList = []
nonGeoTotal = 0

for subdir, dirs, files in os.walk(rootdir):
    for tcpFile in files:

        fullLocation = os.path.join(subdir, tcpFile)
        tcpTest = isFileTCP(fullLocation)
        
        if tcpTest is True:

            checkTCP = tcpCheck(fullLocation)
            tcp = tcpFormatter(checkTCP.dict(), latLngFix=True)
            geoJson = geoJsonFormatter(tcpDict=tcp.dict(), fileLocation=fullLocation).dict()

            if geoJson["geometry"]["coordinates"][0] == -108.601:
                nonGeoList.append(fullLocation)
                nonGeoTotal += 1
                logging.warning(f'NON GEOREF: {fullLocation}')

            tcpList.append(geoJson)
            tcpTotal += 1
            logging.info(f'TCP: {tcpFile}')

        else:
            nonTCPList.append(fullLocation)
            nonTCPTotal += 1
            logging.warning(f'NON TCP: {tcpFile}')

# Save The List Of Processed TCP Files
saveToJson(tcpList)
# Save The GeoJSON Feature Collection To A File
saveGeoJson(featureCollection(tcpList))
# Save The List Of Non TCP & Non Geo Referenced Files
saveErrors(nonTCPTotal, nonTCPList, nonGeoTotal, nonGeoList)

print(f"""\

    ################## ~ COMPLETED ~ ##################
    #                                                 #
        Total Files Processed: {tcpTotal}
    #                                                 #
        Total Non GeoReferenced TCPs: {nonGeoTotal}
    #                                                 #
        Total Non TCPs: {nonTCPTotal}
    #                                                 #
    ###################################################
    """)

input("Press Any Key to Exit...")
