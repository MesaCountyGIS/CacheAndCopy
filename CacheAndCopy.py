## -*- coding: utf-8 -*-                                                                    
## ---------------------------------------------------------------------------              
## Label_Cache.py                                                                          
## Created on: 2014-04-17                                                 
## Created by Ryan Davison & Chris Kadel                                                
## Description: Process to update a service cache from a staging server to a production
## server
## ---------------------------------------------------------------------------            
##############################################################################################



# Import arcpy module
import arcpy, shutil, os, sys, time, datetime



#### Create variables ####

## Replace the path below with the path to your staging server service's _alllayers folder.
stagingServerLevelFoldersLocation = "[Your local drive letter on staging server]:\\arcgisserver\\directories\\arcgiscache\\[Your Map Service Name]\\Layers\\_alllayers"

## Replace the path below with the path to your production server services Layers folder (not all the way to the _alllayers folder)
productionServerLayersFoldersLocation = "[Your local drive letter on production server]:\\arcgisserver\\directories\\arcgiscache\\[Your Map Service Name]\\Layers"

## Replace the path below with the path to your staging server's ArcGIS connection file
connectionFile = r"[Your local drive letter]:\Users\[Your OS user name]\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\\"

## Replace the path below with the path to your staging server's ArcGIS Server admin connection
server = "[Your server name] (admin)"

## Replace the path below
serviceName = "\\[Your service name].MapServer"

inputService = connectionFile + server + serviceName

currentTime = datetime.datetime.now()
thisDate = currentTime.strftime("%Y-%m-%d %H:%M")

## Replace the path below to point to a location where the script report 
reportfile = r'C:/[An arbitrary folder location]/report.txt'

## Enter the scales at which you will be caching. The scales entered below are for example only
firstCacheScales = [1000000,500000,250000,125000,64000,32000,16000,8000]

## Enter scales for use in a second cache
"""You might want to do this if you are caching a large area and
you only want to cache the small scales at the full extent but
you want to cache larger scales within a smaller extent.
The scales entered below are for example only"""
secondCacheScales = [4000,2000,1000,500,275]

## Enter an area of interest (extent) for the cache to be constrained by.
## The extent entered below is for example only
firstAOI = "242775.500086904 4096010.49988047 1280021.731 4650654.00012982"

## Enter an area of interest (extent) for the secondary cache to be constrained by if you are using one.
## The extent entered below is for example only
secondAOI = "667911.625 4263095 812502.125 4363489.5"

#### End create variables section ####



#calculate the number of hours various sections of the code take to run
def convertTime(seconds)
    hours = (seconds/60)/60
    return hours

print convertTime(7254)

#print results of the script to a report
report = open(reportfile,'w')

try:
    #Start the main timer
    startTime = time.time()

    #Create the _alllayers folder in the c drive for arcServer to generate the new cache into
    os.makedirs(stagingServerLevelFoldersLocation)

    #Run the higher level cache layers at the full extent of all SDE data (time this process)
    startFirstCache = time.time()
    arcpy.ManageMapServerCacheTiles_server(inputService, firstCacheScales, "RECREATE_ALL_TILES", "2", "", firstAOI, "WAIT")
    finishFirstCache = time.time()

    ##Uncomment the lines below to run the ManageMapServerCacheTiles_server a second time if you want to run certain scale levels at a different extent
##    startSecondCache = time.time()
##    arcpy.ManageMapServerCacheTiles_server(inputService, secondCacheScales, "RECREATE_ALL_TILES", "2", "", secondAOI, "WAIT")
##    finishSecondCache = time.time()

    #create a reference to a temporary _alllayers directory then rename the populated _alllayers to _alllayers_old
    temporaryStagingFolderRename = "C:\\arcgisserver\\directories\\arcgiscache\\maps_parcel_road_labels\\Layers\\_alllayers_temp"
    os.rename(stagingServerLevelFoldersLocation, stagingServerLevelFoldersLocation + "_temp")

    #Use shutil.rmtree to remove the _alllayers_old folder on the destination server
    shutil.rmtree(productionServerLayersFoldersLocation + "\\_alllayers_old")

    #Move the renamed and current cache folder (_alllayers_temp) over to the production server
    startMove = time.time()
    shutil.move(temporaryStagingFolderRename, productionServerLayersFoldersLocation)
    endMove = time.time()

    #Rename the current production cache directory to _alllayers_old
    os.rename(productionServerLayersFoldersLocation + "\\_alllayers", productionServerLayersFoldersLocation + "\\_alllayers_old")
    #Sleep for 30 seconds to ensure the rename finishes before the next step (probably not necessary but we had issues with this happening. Those issues did not return after implementing the sleep)
    time.sleep(30)
    #Rename the newly copied over _the alllayers_temp directory to _alllayers. This causes it to become the current production cache directory
    os.rename(productionServerLayersFoldersLocation + "\\_alllayers_temp", productionServerLayersFoldersLocation + "\\_alllayers")

    #End the main timer
    finishTime = time.time()

    #calculate process times
    totalElapsedTime = convertTime(finishTime - startTime)
    firstCache = convertTime(finishFirstCache - startFirstCache)

    #Uncomment the line below if you are using a secondary cache process form above  
##    secondCache = convertTime(finishSecondCache - startSecondCache)
    moveCache = convertTime(endMove - startMove)

    #Write process times and completed date to the text report
    report.write("Process completed in: " + str(totalElapsedTime) + " hours\nFirst cache completed in: " + str(firstCache) + " hours\n" +
##    Uncomment the line below if you are running a secondCache above             
##                 "Low level cache completed in: " + str(secondCache) +  "hours\n" +
                 "Moving the cache took: " + str(moveCache) + " hours\nDate Completed: " + str(thisDate))

except Exception, e:
    print e
    #If an error occurred, print line number and error message
    tb = sys.exc_info()[2]
    report.write("Failed at \n" "Line %i" % tb.tb_lineno)
    report.write(e.message)

report.close()
print "report closed"





