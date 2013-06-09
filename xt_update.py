#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the shelx-2013 in the c:\bn\sxtl directory

import urllib2
import time
import os
import sys
import tempfile
import zipfile
from subprocess import call
import getpass
import shutil
import platform

username = sys.argv[1]
passwd = sys.argv[2]
timestr = time.strftime("%Y%m%d")

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

platform = platform.architecture()
print 'Pulling '+platform[0]+' version'
if platform[0] == '32bit':
    filename = "shelxt.exe"
if platform[0] == '64bit':
    filename = "shelxt64.exe"


fileurl = 'http://shelx.uni-ac.gwdg.de/shelxt-beta/'+filename
top_level_url = 'http://shelx.uni-ac.gwdg.de/shelxt-beta/'
installdir = 'c:\\bn\\sxtl\\'


print "Installing in:", installdir

def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0
   data = []

   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      data += chunk
      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   return "".join(data)

   response = urllib2.urlopen(top_level_url);
   chunk_read(response, report_hook=chunk_report)


# create a password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
password_mgr.add_password(None, top_level_url, username, passwd)

handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)

# use the opener to fetch a URL
opener.open(fileurl)

# Install the opener.
# Now all calls to urllib2.urlopen use our opener.
urllib2.install_opener(opener)


if __name__ == '__main__':
    
    req = urllib2.Request(fileurl)
    response = urllib2.urlopen(req)
    the_file = chunk_read(response, report_hook=chunk_report)
    
    #Save the file in the actual directory
    localFile = open(filename, 'wb')
    localFile.write(the_file)
    localFile.close()
    
    
    #make copys of the files with "Bruker names"
    shutil.copy(filename, installdir+'/shelxt.exe')
    shutil.copy(filename, installdir+'/xt.exe')
    
    # Cleaning up
    actualpath = sys.path[0]
    os.chdir(actualpath)
    os.remove(filename) 
    
        
        
        