import re, sqlite3, datetime

# from http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
def num (s):
    try:
        return int(s)
    except exceptions.ValueError:
        return float(s)

def FLEXLMLOG2DB(inputfilename, outputfilename):
   "Convert lines from a FlexLM debug log to a database format"
   inputfile = open(inputfilename, "r")
   logoutputfile = open(outputfilename + '.log', "w")
   conn = sqlite3.connect(outputfilename)
   
   cursor = conn.cursor()
 
   # drop table if it exists
   cursor.execute("""
                   DROP TABLE IF EXISTS flusagelog 
                  """)
 
   # create a table
   cursor.execute("""
                  CREATE TABLE flusagelog
                  (logyear integer, logmonth integer, logday integer,
                   loghour integer, logminute integer, logsecond integer,
                   username text, useronly text, userhostonly text, licensemode text, licensename text,
                   dt timestamp) 
                  """)
   
   computername = ""
   logdate = ""
   logtime = ""
   licensemode = ""
   username = ""
   for line in inputfile:
    logtime = line[0:8]
    if re.match(".*FLEXnet Licensing.*started on.*", line):
      startcomputername = line.index(' ',line.index("started on")+len("started on"))+1
      endcomputername = line.index(' ', startcomputername+1)
      computername = line[startcomputername:endcomputername]
      endlogdate = line.rindex(')')
      startlogdate = line.rindex('(')+1
      logdate = line[startlogdate:endlogdate]
    if re.match(".* OUT: .*", line):
      licensemode = "OUT"
      licensenamestart = line.index('"', line.index("OUT:")) + 1
      licensenameend = line.index('"', licensenamestart)
      licensename = line[licensenamestart:licensenameend]
      usernamestart = line.index(' ', licensenameend)+1
      usernameend = line.index(' ', usernamestart)
      username = line[usernamestart:usernameend].rstrip()
    else:  
      if re.match(".* IN: .*", line):
        licensemode = "IN"
        licensenamestart = line.index('"', line.index("IN:")) + 1
        licensenameend = line.index('"', licensenamestart)
        licensename = line[licensenamestart:licensenameend]
        usernamestart = line.index(' ', licensenameend)+1
        usernameend = line.index(' ', usernamestart)
        username = line[usernamestart:usernameend].rstrip()
      else:
        licensemode = ""
        licensename = ""
        username = ""

    if licensemode != "" and licensename != "" and username != "":
      logyear = logdate[logdate.rindex('/')+1:].strip().zfill(4)
      logmonth = logdate[:logdate.index('/')].strip().zfill(2)
      logday = logdate[logdate.index('/')+1:logdate.rindex('/')].strip().zfill(2)
      loghour = logtime[:logtime.index(':')].strip().zfill(2)
      logminute = logtime[logtime.index(':')+1:logtime.rindex(':')].strip().zfill(2)
      logsecond = logtime[logtime.rindex(':')+1:].strip().zfill(2)
      useronly = username[:username.index('@')].strip()
      userhostonly = username[username.index('@')+1:].strip()
      logoutputfile.write(logyear + ',' + logmonth + ',' + logday + ',' + loghour + ',' + logminute + ',' + logsecond + ',' +  username + ',' + useronly + ',' + userhostonly + ',' + licensemode + ',' + licensename + '\n')
      cursor.execute('insert into flusagelog values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (logyear, logmonth, logday, loghour, logminute, logsecond, username, useronly, userhostonly, licensemode, licensename, datetime.datetime(num(logyear), num(logmonth), num(logday), num(loghour), num(logminute), num(logsecond))))

   conn.commit()
   
   inputfile.close()
   logoutputfile.close()
   return;