CacheAndCopy
============

Python script to run an ArcGIS server cache on a staging server then copy it to a production server

Ryan Davison gis@mesacounty.us

2014-05-23

At Mesa County we do a lot of caching of ArcGIS services for our web applications. Some of our vector caches need to be updated on a regular basis. Because of the large extent of the county, these vector caches can be fairly large and take a lot of time to complete.

Rather than run a resource-hogging cache process on our production server and risk our users having a degraded experience we cache on a staging server and then copy the layer level folders (L00, L01, L02...) to the production server that already has an identical service prepared with the same tiling scheme as the cached service on the staging server.

CacheAndCopy.py automates this process when you use it with Task Scheduler or Chron.

To get CacheAndCopy up and running on your staging server you just need to replace the paths for a few variable in the script:

stagingServerLevelFoldersLocation = "[Your local drive letter on staging server]:\arcgisserver\directories\arcgiscache\[Your Map Service Name]\Layers\_alllayers" productionServerLayersFoldersLocation = "[Your local drive letter on production server]:\arcgisserver\directories\arcgiscache\[Your Map Service Name]\Layers" connectionFile = r"[Your local drive letter]:\Users[Your OS user name]\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\" server = "Your server name" serviceName = "\[Your service name].MapServer" reportfile = r'C:/[An arbitrary folder location]/report.txt' firstCacheScales = [[Add your scale levels here]] firstAOI = "[Enter an area of interest (map extent)]"
