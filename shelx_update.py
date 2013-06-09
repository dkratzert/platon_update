#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the shelx in the c:\bn\sxtl directory

import urllib2
import time
import os
import sys
import tempfile
import zipfile
from subprocess import call
import getpass
import shutil


username = sys.argv[1]
passwd = sys.argv[2]
timestr = time.strftime("%Y%m%d")

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

filename = "install_shelx_win64.exe"
fileurl = 'http://shelx.uni-ac.gwdg.de/~gsheldr/bin/install_shelx_win64.exe'
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


   response = urllib2.urlopen('http://www.ebay.com');
   chunk_read(response, report_hook=chunk_report)


# create a password manager
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
top_level_url = 'http://shelx.uni-ac.gwdg.de/~gsheldr/bin/'
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
    if not os.path.isfile(filename):
        req = urllib2.Request(fileurl)
        response = urllib2.urlopen(req)
        the_file = chunk_read(response, report_hook=chunk_report)

        # Just create a temporary file and dont keep it
        #localFile = tempfile.TemporaryFile()
        #localFile.write(the_file)
        #localFile.close()
        
        print os.path.isfile(filename)
        #Save the file in the actual directory
        localFile = open(filename, 'wb')
        localFile.write(the_file)
        localFile.close()
    else:
        #/D destination
        #/S silent
        #params = '/S ' +' /D='+installdir  #This doesn't work
        params = '/S'
        print 'Installing with parameter: ' +params +'\n'
        call([filename, params])
        installpath = 'C:\\Users\\' +getpass.getuser() +'\\AppData\\Local\\shelx64' 
        
        os.chdir(installpath)
        os.remove('./Uninstall.exe')
        for files in os.listdir("."):
            if files.endswith(".exe"):
                #print files
                print 'Installing '+files +' in ' +installdir
                shutil.copy(files, installdir)
                
        shutil.copy(installdir+'/shelxl.exe', installdir+'/xl.exe')
        shutil.copy(installdir+'/shelxd.exe', installdir+'/xd.exe')
        shutil.copy(installdir+'/shelxs.exe', installdir+'/xs.exe')
        shutil.copy(installdir+'/ciftab.exe', installdir+'/xcif.exe')
        
        os.remove(filename) 
        
        
        
        