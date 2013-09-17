#!/usr/bin/python

import sys, getopt, os.path, os, re

from changetext import *

def util_fileexists(inputfile):
   fileexists = os.path.exists(inputfile)
   try:
     with open(inputfile): pass
   except IOError:
     fileexists = False
   return fileexists;

def print_moruga_help():
   print ' moruga.py -m <mode> -i <inputfile> -o <outputfile>'
   print '   where <mode> is one of: COPY,MAPPROXYGC,WIKIXML2TW'
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
       functiontocall = getattr(getattr(sys.modules["changetext"], "%s" % fixmode), "%s" % fixmode)
       functiontocall(inputfile, outputfile)
       print os.linesep, ' Done.'
     except:
       exc_type, exc_value, exc_traceback = sys.exc_info()
       print exc_type, exc_value, exc_traceback
       print os.linesep, ' Error 06 - Unable to find mode function '
       print_moruga_help()  
       sys.exit(6)       
   return;

def main(argv):
   inputfile = ''
   outputfile = ''
   changemode = ''
   print os.linesep, ' Moruga - Text manipulator - Version 0.2 - b20130916'
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
