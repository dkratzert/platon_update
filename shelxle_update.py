#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the shelx-2013 in the c:\bn\sxtl directory

import os
import sys
import urllib2
from _winreg import *
import shutil
import win32com.shell.shell as shell

revurl = 'http://ewald.ac.chemie.uni-goettingen.de/shelx/revision.php'
params = '/S'
    
def revision():
    response = urllib2.urlopen(revurl)
    rev = response.read()
    return rev

version = revision()
file = "shelxle.exe"
url = 'http://sourceforge.net/projects/shelxle/files/windows/\
winshelx_setup-1.0.'+version+'.exe/download'

#Writing standard install directory to registry
#C:\Program Files\shelxle
aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
aKey = OpenKey(aReg, r"Software\shelxle", 0, KEY_WRITE)
SetValueEx(aKey,"",0, REG_SZ, r"C:\Program Files\shelxle")


# reports the downloaded chuncs to the screen
def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 1)
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
    
    response = urllib2.urlopen(url);
    chunk_read(response, report_hook=chunk_report)

print 'Downloading revision '+revision()+'\n'

req = urllib2.Request(url)
response = urllib2.urlopen(req)

#download the file   
#try:
#    #Save the file in the actual directory
#    the_file = chunk_read(response, report_hook=chunk_report)
#    localFile = open(file, 'wb')
#    localFile.write(the_file)
#    localFile.close()
#except KeyboardInterrupt:
#    print "\naborted!"
#    sys.exit()

 
# Installing
print 'Installing with parameter: ' +params +'\n'
# we need this for the UAC to elevate the user previleges
shell.ShellExecuteEx(lpVerb='runas', lpFile=file, lpParameters=params)
#cleaning up
os.remove(file) 
