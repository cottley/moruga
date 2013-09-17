    
def WIKIXML2TW(inputfilename, outputfilename):
   "Convert Wikimedia XML dump to TiddlyWiki import file"
   inputfile = open(inputfilename, "r")
   xmlinput = unicode(inputfile.read(), errors='ignore')
   outputfilemenu = open(outputfilename + '.menu', "w")
   outputfile = open(outputfilename, "w")
   outputfile.write('<html><head></head><body><div id="storeArea">'.encode('utf-8'))
   startpos = 0
   
   while startpos > -1:
     titleString = ''
     textString = ''
     startpos = xmlinput.find('<title>', startpos)
     if startpos > -1:
       titleString = xmlinput[startpos+len('<title>'):xmlinput.find('</title>', startpos)]
     if startpos > -1:
       startpos = xmlinput.find('</title>', startpos)
     if startpos > -1:
       startpos = xmlinput.find('<text xml:space="preserve">', startpos)
     if startpos > -1:
       textString = xmlinput[startpos+len('<text xml:space="preserve">'):xmlinput.find('</text>', startpos)]
     if startpos > -1:
       startpos = xmlinput.find('</text>', startpos)
     if titleString != '':
       originalTitleString = titleString
       titleString = titleString.replace(' ', '_')
       outputfile.write('<div title="'.encode('utf-8'))
       outputfile.write(titleString.encode('utf-8'))
       outputfilemenu.write('[[' + originalTitleString + '|' + titleString.encode('utf-8') + ']]\n')
       outputfile.write('" creator="YourName" modifier="YourName" created="201309161317" modified="201309161321" tags="MediaWikiFormat" changecount="1"><pre>'.encode('utf-8'))
       outputfile.write(textString.encode('utf-8'))
       outputfile.write('</pre></div>\n'.encode('utf-8'))

   outputfile.write('</div></body></html>'.encode('utf-8'))
   outputfile.close()
   outputfilemenu.close()
   return;