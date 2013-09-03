#!/usr/bin/python

import sys, getopt, os.path, os, re, yaml


def changetext_MAPPROXYGC(inputfilename, outputfilename):
   "Convert a GetCapabilities MapProxy-util dump to a MapProxy configuration"
  
   inputfile = open(inputfilename, "r")
   outputfile = open(outputfilename, "w")

   try:
     dataMap = yaml.safe_load(inputfile)
   
     str = ""
     str += "services:"
     str += "\n  demo:"
     str += "\n  kml:"
     str += "\n  tms:"
     str += "\n    # needs no arguments"
     str += "\n  wmts:"
     str += "\n  wms:"
     str += "\n    md:"
     str += "\n      # metadata used in capabilities documents"
     str += "\n      title: " + dataMap["Root-Layer"][0]["title"]
     str += "\n      abstract: MapProxy based software distribution"
     str += "\n      online_resource: http://mapproxy.org/"
     str += "\n      contact:"
     str += "\n        person: Put your name here"
     str += "\n        position: Put your position here"
     str += "\n      access_constraints:"
     str += "\n        Persisting map tiles locally breaks the terms of service for many popular basemap providers like Google, Bing, and ArcGIS Online."
     str += "\n        If you use MapProxy to access and store tiles offline without permission, then you do so at your own risk."
     str += "\n      fees: 'None'"
     str += "\n"
     str += "\nlayers:"
    
     for layer in dataMap["Root-Layer"][0]["layers"]:
       str += "\n  - name: " + layer["name"]
       str += "\n    title: " + layer["title"]
       str += "\n    sources: [" + layer["name"] + "_cache]"
     
     str += "\n"
     str += "\ncaches:"
     
     for layer in dataMap["Root-Layer"][0]["layers"]:     
       str += "\n  " + layer["name"] + "_cache:"
       str += "\n    grids: [" + layer["name"] + "_grid]"
       str += "\n    sources: [" + layer["name"] + "]"

     str += "\n"
     str += "\nsources:"
     
     for layer in dataMap["Root-Layer"][0]["layers"]: 
       str += "\n  " + layer["name"] + ":"
       str += "\n    type: wms"
       layersrs = "["
       # for srsentry in layer["srs"]:
         # if layersrs != "[":
           # layersrs += ", "
         # layersrs += "'" + srsentry + "'"
       # layersrs += "]"  
       # str += "\n    supported_srs: " + layersrs
       str += "\n    req:"
       str += "\n      url: " + layer["url"]
       str += "\n      layers: " + layer["name"]

     str += "\n"
     str += "\ngrids:"
     
     for layer in dataMap["Root-Layer"][0]["layers"]: 
       str += "\n  " + layer["name"] + "_grid:"
       str += "\n    base: GLOBAL_MERCATOR"
       str += "\n    origin: ul"
    
     str += "\n"
     str += "\nglobals:"
     str += "\n  # # coordinate transformation options"
     str += "\n  # srs:"
     str += "\n  #   # WMS 1.3.0 requires all coordiates in the correct axis order,"
     str += "\n  #   # i.e. lon/lat or lat/lon. Use the following settings to"
     str += "\n  #   # explicitly set a CRS to either North/East or East/North"
     str += "\n  #   # ordering."
     str += "\n  #   axis_order_ne: ['EPSG:9999', 'EPSG:9998']"
     str += "\n  #   axis_order_en: ['EPSG:0000', 'EPSG:0001']"
     str += "\n  #   # you can set the proj4 data dir here, if you need custom"
     str += "\n  #   # epsg definitions. the path must contain a file named 'epsg'"
     str += "\n  #   # the format of the file is:"
     str += "\n  #   # <4326> +proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs  <>"
     str += "\n  #   proj_data_dir: '/path to dir that contains epsg file'"
     str += "\n"
     str += "\n  # # cache options"
     str += "\n  cache:"
     str += "\n    # where to store the cached images"
     str += "\n    base_dir: './cache_data'"
     str += "\n    # where to store lockfiles"
     str += "\n    lock_dir: './cache_data/locks'"
     str += "\n  #   # request x*y tiles in one step"
     str += "\n  #   meta_size: [4, 4]"
     str += "\n  #   # add a buffer on all sides (in pixel) when requesting"
     str += "\n  #   # new images"
     str += "\n  #   meta_buffer: 80"
     str += "\n"
     str += "\n"
     str += "\n  # image/transformation options"
     str += "\n  image:"
     str += "\n      #resampling_method: nearest"
     str += "\n      # resampling_method: bilinear"
     str += "\n       resampling_method: bicubic"
     str += "\n  #     jpeg_quality: 90"
     str += "\n  #     # stretch cached images by this factor before"
     str += "\n  #     # using the next level"
     str += "\n  #     stretch_factor: 1.15"
     str += "\n  #     # shrink cached images up to this factor before"
     str += "\n  #     # returning an empty image (for the first level)"
     str += "\n  #     max_shrink_factor: 4.0"
     str += "\n"
       
     outputfile.write(str)
   except:
     print os.linesep, ' Error MAPPROXY01 - Unable to process file as YAML '
   inputfile.close()
   outputfile.close()
   return;

def changetext_COPY(inputfilename, outputfilename):
   "Copy the lines from input to output"
   inputfile = open(inputfilename, "r")
   outputfile = open(outputfilename, "w")
   for line in inputfile:
      outputfile.write(line)
   inputfile.close()
   outputfile.close()
   return;

def util_fileexists(inputfile):
   fileexists = os.path.exists(inputfile)
   try:
     with open(inputfile): pass
   except IOError:
     fileexists = False
   return fileexists;

def print_moruga_help():
   print ' moruga.py -m <mode> -i <inputfile> -o <outputfile>'
   print '   where <mode> is one of: COPY,MAPPROXYGC'
   return;


def processfilewithmode( fixmode, inputfile, outputfile ):
   "Tries to fix the input file using fix mode to create the output file"
   if fixmode == '':
     print os.linesep, ' Error 03 - Fix mode must be specified to do conversion '
     print_moruga_help()
     sys.exit(3)
   elif not util_fileexists(inputfile):
     print os.linesep, ' Error 04 - Input file must exist '
     print_moruga_help()
     sys.exit(4)
   elif outputfile == '':
     print ''
     print ' Error 05 - Output file must be specified '
     print_moruga_help()
     sys.exit(5)
   else:
     try:
       functiontocall = getattr(sys.modules[__name__], "changetext_%s" % fixmode)
       functiontocall(inputfile, outputfile)
       print os.linesep, ' Done.'
     except:
       print os.linesep, ' Error 06 - Unable to find mode function '
       print_moruga_help()  
       sys.exit(6)       
   return;

def main(argv):
   inputfile = ''
   outputfile = ''
   changemode = ''
   print os.linesep, ' Moruga - Text manipulator - Version 0.1 - b20130902'
   print ' by Christopher Ottley'
   print ' ========================================'
   print os.linesep
   try:
      opts, args = getopt.getopt(argv,"hm:i:o:",["mode=","ifile=","ofile="])
   except getopt.GetoptError:
      print_moruga_help()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print_moruga_help()
         sys.exit()
      elif opt in ("-m", "--mode"):
         changemode = arg         
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print '  Change mode is',changemode
   print '   Input file is',inputfile
   print '  Output file is',outputfile
   processfilewithmode(changemode, inputfile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
