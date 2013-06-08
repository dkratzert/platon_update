#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the platon.exe in the c:\pwt directory

#http://www.cryst.chem.uu.nl/spek/xraysoft/mswindows/platon/platon.zip

import urllib2
import time
import os
import tempfile
import zipfile

timestr = time.strftime("%Y%m%d")

u = urllib2.urlopen('http://www.cryst.chem.uu.nl/spek/xraysoft/mswindows/platon/platon.zip')


#File = 'platon-%s.zip' %timestr
#print '%20s  %s' % (File, zipfile.is_zipfile(File))

localFile = tempfile.TemporaryFile()
localFile.write(u.read())
#localFile.close()

zf = zipfile.ZipFile(localFile, 'r')

list = zf.namelist()  #list of files in the zipfile
#print list

for name in list:
	fd = open('c:/pwt/'+name, "wb")
	#print fd
	fd.write(zf.read(name))
	print 'extracting', name
	fd.close()

#os.remove(File)
