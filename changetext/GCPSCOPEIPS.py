import json

def GCPSCOPEIPS(inputscope, outputfilename):
   "Extracting us-central1 scope IP address ranges"
   outputfile = open(outputfilename, "w")
   outputfile.write('ip4Prefixes for us-central1\n')
   with open(inputscope) as f:
     data = json.load(f)
     for prefix in data['prefixes']:
       if prefix['scope'] == 'us-central1':
         outputfile.write(prefix['ipv4Prefix'] + '\n')
   outputfile.close()
   return;