#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the platon.exe in the c:\pwt directory

import urllib2
import os
import tempfile
import zipfile

u = urllib2.urlopen('http://www.cryst.chem.uu.nl/spek/xraysoft/mswindows/platon/platon.zip')

#create a temporary file and download platon to it.
localFile = tempfile.TemporaryFile()
localFile.write(u.read())

#open the zip file
zf = zipfile.ZipFile(localFile, 'r')

#list of files in the zipfile
list = zf.namelist()  

# extract the files to the platon directory
for name in list:
	fd = open('c:/pwt/'+name, "wb")
	fd.write(zf.read(name))
	print 'extracting', name
	fd.close()

localFile.close()