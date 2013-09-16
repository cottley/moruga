
def COPY(inputfilename, outputfilename):
   "Copy the lines from input to output"
   inputfile = open(inputfilename, "r")
   outputfile = open(outputfilename, "w")
   for line in inputfile:
      outputfile.write(line)
   inputfile.close()
   outputfile.close()
   return;