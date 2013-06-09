#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the shelt-2013 in the c:\bn\sxtl directory

import urllib2
import os
import sys
from subprocess import call
import getpass
import shutil
import platform
from argparse import ArgumentParser

# options parser for username and password of the download
parser = ArgumentParser(description='This script fetches the current version of SHELXT-2013 \
            and installs it into c:\\bn\\SXTL. The xt.exe is also updated')
parser.add_argument("-u", dest="username", metavar='username', help="A user name is required \
            to download SHELX-2013")
parser.add_argument("-p", dest="password", metavar='password', help="A password is required \
            to download SHELXT-2013")
options = parser.parse_args()

if options.username is None:
	print "\nPlease give the user name as argument!\n"
	parser.print_help()
	sys.exit(-1)
elif options.password is None:
	print "\nPlease give the password as argument!\n"
	parser.print_help()
	sys.exit(-1)

username = options.username
passwd = options.password

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

# we need to know if its 32 or 64 bit
platform = platform.architecture()
print 'Pulling '+platform[0]+' version'

# decide which platform to use
if platform[0] == '32bit':
    filename = "shelxt.exe"
if platform[0] == '64bit':
    filename = "shelxt64.exe"


fileurl = 'http://shelx.uni-ac.gwdg.de/shelxt-beta/'+filename
top_level_url = 'http://shelx.uni-ac.gwdg.de/shelxt-beta/'
installdir = 'c:\\bn\\sxtl\\'

print "Installing in:", installdir


# reports the downloaded chuncs to the screen
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
try:
    opener.open(fileurl)
except urllib2.HTTPError, e:
    z = e
    print
    print z
    print "Wrong username or password?"
    sys.exit()

# Install the opener.
# Now all calls to urllib2.urlopen use our opener.
urllib2.install_opener(opener)


if __name__ == '__main__':
    
    req = urllib2.Request(fileurl)
    response = urllib2.urlopen(req)
    
    try:
        the_file = chunk_read(response, report_hook=chunk_report)
    except KeyboardInterrupt:
        print "\naborted!"
        sys.exit()
    
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
    
