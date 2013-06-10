#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the shelx-2013 in the c:\bn\sxtl directory

import urllib2
import os
import sys
from subprocess import call
import getpass
import shutil
import platform
from argparse import ArgumentParser
import _winreg

# options parser for username and password of the download
parser = ArgumentParser(description='This script fetches the current version of SHELX-2013 \
            and installs it into c:\\bn\\SXTL. The x[l/d/s].exe and xcif.exe are also updated')
parser.add_argument("-u", dest="username", metavar='username', help="A user name is required \
            to download SHELX-2013")
parser.add_argument("-p", dest="password", metavar='password', help="A password is required \
            to download SHELX-2013")
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
try:
    os.environ["PROGRAMFILES(X86)"]
    platnumber = str(64)
except:
    platnumber = str(32)
print 'Pulling '+platnumber+'bit version'

platform = platnumber+'bit'


# decide which platform to use
if platform == '32bit':
    filename = "install_shelx_win32.exe"
if platform == '64bit':
    filename = "install_shelx_win64.exe"

aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
aKey = OpenKey(aReg, r"HKEY_CURRENT_USER\Software\shelx64") 
key = EnumValue(aKey)
CloseKey(aKey)    

print key
sys.exit()

fileurl = 'http://shelx.uni-ac.gwdg.de/~gsheldr/bin/'+filename
top_level_url = 'http://shelx.uni-ac.gwdg.de/~gsheldr/bin/'
installdir = 'c:\\bn\\sxtl\\'
installpath = 'C:\\Users\\' +getpass.getuser() +'\\AppData\\Local\\shelx'+platnumber

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
    
    #only download if the file is not already there
    if not os.path.isfile(filename):
        req = urllib2.Request(fileurl)
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            z = e
            print
            print z
            print "Wrong username or password?"
            sys.exit()
            
        try:
            the_file = chunk_read(response, report_hook=chunk_report)
        except KeyboardInterrupt:
            print "\naborted!"
            sys.exit()

        #Save the downloaded file in the actual directory
        localFile = open(filename, 'wb')
        localFile.write(the_file)
        localFile.close()
    
    #/D destination   #/S silent
    #params = '/S ' +' /D='+installdir  #This doesn't work
    params = '/S'
    print 'Installing with parameter: ' +params +'\n'
    call([filename, params])
    os.chdir(installpath)
    os.remove('./Uninstall.exe')
    
    for files in os.listdir("."):
        if files.endswith(".exe"):
            #print files
            print 'Installing '+files +' in ' +installdir
            shutil.copy(files, installdir)
            os.remove(files)
    
    #make copys of the files with "Bruker names"
    shutil.copy(installdir+'/shelxl.exe', installdir+'/xl.exe')
    shutil.copy(installdir+'/shelxd.exe', installdir+'/xd.exe')
    shutil.copy(installdir+'/shelxs.exe', installdir+'/xs.exe')
    shutil.copy(installdir+'/ciftab.exe', installdir+'/xcif.exe')
    
    # Cleaning up
    actualpath = sys.path[0]
    os.chdir(actualpath)
    os.remove(filename) 
