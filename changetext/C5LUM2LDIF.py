import json
import random

def C5LUM2LDIF(inputfilename, outputfilename):
   "Converting Concrete5 Lazy User Migrator user and group export to LDIF"
   with open(inputfilename) as f:
     data = json.load(f)
   output_users = {}
   output_groups = {}
   if 'Users' in data:
     sourceUserData = data['Users']
     print('')
     for user in sourceUserData:
       if user['name'] != 'admin':
         print('Converting ' + user['name'])       
         output_users[user['name']] = {}
         for attribute in user['attributes']:
           if 'firstname' in attribute:
             output_users[user['name']]['firstname'] = attribute['firstname']
           if 'surname' in attribute:
             output_users[user['name']]['surname'] = attribute['surname']
         for group in user['groups']:
           for key in group:
             if group[key] in output_groups:
               output_groups[group[key]]['users'].append(user['name'])
             else:
               output_groups[group[key]] = {}
               output_groups[group[key]]['name'] = group[key]
               output_groups[group[key]]['users'] = []
   #print(data)
   outputfile = open(outputfilename, "w")
   outputfile.write('# Concrete5 User and Group LDIF data\n');
   outputfile.write('#\n');
   outputfile.write('# userpassword for all users is "pass"\n');
   outputfile.write('#\n');
   outputfile.write('version: 1\n');
   for user in output_users:
     surname = output_users[user]['surname']
     if surname is None:
       surname = ''
     firstname = output_users[user]['firstname']
     if firstname is None:
       firstname = ''
     fullname = firstname + ' ' + surname
     if fullname == ' ':
       fullname = user
     if firstname == '':
       firstname = user
     if surname == '':
       surname = user
     outputfile.write('\n')
     outputfile.write('dn: uid=' + user + ',ou=EDH,dc=edh,dc=custom,dc=slb,dc=com\n')
     outputfile.write('objectClass: inetOrgPerson\n')
     outputfile.write('objectClass: posixAccount\n')
     outputfile.write('objectClass: top\n')
     outputfile.write('cn: ' + fullname + '\n')
     outputfile.write('gidNumber: 0\n')
     outputfile.write('homeDirectory: /home/' + user + '\n')
     outputfile.write('sn: ' + surname + '\n')
     outputfile.write('uid: ' + user + '\n')
     outputfile.write('uidNumber: ' + str(random.randint(10000, 999999)) + '\n')
     outputfile.write('displayName: ' + fullname + '\n')
     outputfile.write('givenName: ' + firstname + '\n')
     outputfile.write('userPassword:: e1NTSEF9MWhTVWR0cDhMVWR4ZUFVKzBOa1pqT0Vham5aRHV4QzQ=\n')
   outputfile.write('\n\n#\n');
   outputfile.write('# Groups\n');
   outputfile.write('#\n\n');
   for group in output_groups:
     groupname = output_groups[group]['name']
     outputfile.write('\n')   
     outputfile.write('dn: cn=' + groupname + ',ou=EDH,dc=edh,dc=custom,dc=slb,dc=com\n')
     outputfile.write('objectClass: posixGroup\n')
     outputfile.write('objectClass: top\n')
     outputfile.write('cn: ' + groupname + '\n')
     outputfile.write('gidNumber: ' + str(random.randint(10000, 999999)) + '\n')
     outputfile.write('description: ' + groupname + '\n')
     for groupuser in output_groups[group]['users']:
       outputfile.write('memberUid: ' + groupuser + '\n')
   outputfile.close()
   return;