moruga
======

Simple text manipluation with Python. Implement custom functions and call command line with mode switch. The assumption is that both the input file and output are text. 

Call on the command line using switches
  -m MODE
  -i INPUTFILE
  -o OUTPUTFILE

```
moruga.py -m <MODE> -i <INPUTFILE> -o <OUTPUTFILE>
```

Mode COPY
---------

This mode is a test mode that copies the file from input file to output file. 

Mode MAPPROXYGC
---------------
MapProxy has the ability since version 1.5.0 to create a YAML configuration file from a WMS URL. Unfortunately, while the output of this utlity function is a good starting point, it doesn't create a mapproxy configuration file. The MAPPROXYGC mode is designed to do a simple creation of a mapproxy configuration file from the output of the mapproxy wms-capabilites mode. If we have a WMS service at http://my.wms.server/wms.ashx?REQUEST=GetCapabilities we can get the output from the command line via a redirect as seen below: 

```
mapproxy-util wms-capabilities http://my.wms.server/wms.ashx?REQUEST=GetCapabilities > wmsoutput.txt
```

After we get the output we can convert it using a command like below:

```
moruga.py -m MAPPROXYGC -i wmsoutput.txt -o mapproxy.yaml
```