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

username = sys.argv[1]
passwd = sys.argv[2]
timestr = time.strftime("%Y%m%d")

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

fileurl = 'http://shelx.uni-ac.gwdg.de/~gsheldr/bin/install_shelx_win64.exe'

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



localFile = tempfile.TemporaryFile()
localFile.write(opener.read())