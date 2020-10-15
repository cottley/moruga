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

Mode WIKIXML2TW
---------------
MediaWiki (http://www.mediawiki.org/) has the ability to export all of the current revisions of pages to an XML file containing the original Wiki syntax content. This mode allows you to take the XML file as input and create an HTML file as output. The HTML file can be imported into a TiddlyWiki (http://tiddlywiki.com/) configured with the MediaWiki plugins available at http://svn.tiddlywiki.org/Trunk/contributors/MartinBudden/formatters/ . More specifically, install the plugins MediaWikiFormatterPlugin ( http://svn.tiddlywiki.org/Trunk/contributors/MartinBudden/formatters/MediaWikiFormatterPlugin.js) and MediaWikiTableFormatterPlugin ( http://svn.tiddlywiki.org/Trunk/contributors/MartinBudden/formatters/MediaWikiTableFormatterPlugin.js) into TiddlyWiki before importing.

Once run, the output HTML file can be imported using the import function of the TiddlyWiki backstage access.

```
moruga.py -m WIKIXML2TW -i mediawiki.xml -o tiddlywikiimport.html
```

This command also creates a .menu file with the name of the HTML file which can be used to modify the menu entry in the TiddlyWiki. In the above example the .menu file would be named tiddlywikiimport.html.menu.

Mode C5LUM2LDIF
---------------

This mode converts extracted JSON user and group information from the Concrete5 based LazyUserMigrator into an LDIF file that can be imported into OpenLDAP.

User ids and group ids are generated randomly. The administrator user, admin, is excluded and customization of the base DN would need to be done to match the base dn of the OpenLDAP server to be used.

```
moruga.py -m C5LUM2LDIF -i c5usergroups.json -o usergroups.ldif
```

Mode GCPSCOPEIPS
----------------

Google Cloud Platform provides a list of ip addresses (https://www.gstatic.com/ipranges/cloud.json) that indicate the IP address ranges for specific data centers.

This mode allows the extraction of IP addresses for the us-central1 and outputs a text file with those IP address ranges. Download the cloud.json file (for example, using wget) and create the extract using the following command.

```
moruga.py -m GCPSCOPEIPS -i cloud.json -o uscentral1.csv
```

