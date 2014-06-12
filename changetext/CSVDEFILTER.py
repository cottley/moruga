import re
import io
import csv

def CSVDEFILTER(inputfilename, outputfilename):
   "Change CSVDE output CSV file to simple user based CSV file for import"
   inputfile = open(inputfilename, "r")
   outputfile = open(outputfilename, "w")
   scsv = ''
   for line in inputfile:
      if re.search(",user,", line):
        scsv += line + '\n'
   f = io.StringIO(scsv)
   reader = csv.reader(f, delimiter=',')
   outputfile.write('objectClass,sAMAccountName,dn')
   for row in reader:
      if (len(row) > 0):
          if (row[50] != ''):
              if (not row[50].startswith('CN=')):
                  outputfile.write('\n' + row[1] + ',' + row[82] + '," ' + row[0] + '"')
   inputfile.close()
   outputfile.close()
   return;