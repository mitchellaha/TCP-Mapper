import os
from TCPMAPPER.programTitle import programTitle
from TCPMAPPER.TCP import TCP

# Create a folder named TCPMAPPER if it doesnt exist already
outputFolderName = "TCPMAPPER_OUTPUT"
try:
    os.mkdir(os.path.join(os.getcwd(), outputFolderName))
except FileExistsError:
    pass

print(programTitle)
dir = input('Enter the file to process: ')


tcp = TCP(dir)
tcpDict = tcp.dict()
with open(os.path.join(os.getcwd(), outputFolderName, f"{tcp.FileName}.json"), 'w') as f:
    f.write(tcp.json())
    f.close()


devCount = 1
print(f"""\

    ################## ~ COMPLETED ~ ##################
    #                                                 #
        Total Files Processed: {devCount}
    #                                                 #
        Total Non GeoReferenced TCPs: {devCount}
    #                                                 #
        Total Non TCPs: {devCount}
    #                                                 #
    ###################################################
    """)

input("Press Any Key to Exit...")
