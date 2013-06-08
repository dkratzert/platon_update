#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the shelx in the c:\bn\sxtl directory

import urllib2
import time
import os
import tempfile
import zipfile


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
opener.open('http://shelx.uni-ac.gwdg.de/~gsheldr/bin/install_shelx_win64.exe')

timestr = time.strftime("%Y%m%d")

localFile = tempfile.TemporaryFile()
localFile.write(opener.read())