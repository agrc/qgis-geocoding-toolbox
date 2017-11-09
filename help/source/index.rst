.. AGRCGeocodingToolbox documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AGRCGeocodingToolbox's documentation!
============================================

Users must obtain an ip specific mapserv api key by registering on https://api.mapserv.utah.gov prior to use, as a unique api key is one of the required input parameters for running the tool.

The geocoding tool will produce as output a .csv file with the input unique identifier field, the input address information, and the match results. It also produces a .dbf file with the same information and will provide the user with the option to add this to the current ArcMap project. A user can use the .dbf file to join on the unique record identifier to connect with the original results, and also to Display XYEvents to create a map layer of the results.
