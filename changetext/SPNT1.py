import re

def SPNT1(inputfilename, outputfilename):
   inputfile = open(inputfilename, "r")
   outputfile = open(outputfilename, "w")
   for line in inputfile:
    if re.match("SPNT ", line):
      dot1 = line.index('.')+1
      dot2 = line.index('.',dot1)
      dot3 = line.index('.',dot2+4)
      dot4 = line.index('.',dot3+1)-1
      firstnum = line[dot1:dot2].ljust(9)
      secondnum = line[dot2+4:dot3].ljust(15)
      endline = line[dot4:]
      #fixedline = line[:23] + '   ' + line[25:31] + '	   ' + line[35:42] + line[45:]
      fixedline = line[:23] + '   ' + firstnum + ' ' + secondnum + endline
      outputfile.write(fixedline)
    else:
      outputfile.write(line)
   inputfile.close()
   outputfile.close()
   return;