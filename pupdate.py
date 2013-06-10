#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the platon.exe in the c:\pwt directory

import urllib2
import os
import sys
import tempfile
import zipfile
from HTMLParser import HTMLParser


# fetch the changes of platon and store it in one string (text)
html = urllib2.urlopen('http://www.cryst.chem.uu.nl/spek/xraysoft/update_history_platon.html')
text = [html.next() for x in range(15)]
text = "".join(text)

#strips down the html to plain text
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

print strip_tags(text)    
    
sys.exit()
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