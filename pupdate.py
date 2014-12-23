#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the platon.exe in the c:\pwt directory

import urllib2
import os
import sys
import time
import tempfile
import zipfile
from HTMLParser import HTMLParser
import datetime


# fetch the changes of platon and store it in one string (text)
#html = urllib2.urlopen('http://www.cryst.chem.uu.nl/spek/xraysoft/update_history_platon.html')
html = urllib2.urlopen('http://www.platonsoft.nl/spek/xraysoft/mswindows/platon/')
text = [html.next() for x in range(18)]
text = "".join(text)

#strips down the html to plain text
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d.rstrip('\n'))
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

today = datetime.date.today()
print "\nToday is: " +str(today.strftime('%b %d, %Y\n'))
print strip_tags(text)    
    

# now preceed with platon update
u = urllib2.urlopen('http://www.cryst.chem.uu.nl/spek/xraysoft/mswindows/platon/platon.zip')

#create a temporary file and download platon to it.
localFile = tempfile.TemporaryFile()
localFile.write(u.read())

#open the zip file
zf = zipfile.ZipFile(localFile, 'r')

#list of files in the zipfile
list = zf.namelist()  

# if not already present - create the platon directory:
dir = os.path.exists('c:\\pwt')
if not dir:
    try:
        os.mkdir('c:\\pwt')
    except IOError:
        print "unable to create install directory"
        sys.exit()
    else:
        print 'created platon directory c:\\pwt'
        pass
# extract the files to the platon directory
for name in list:
    fd = open('c:/pwt/'+name, "wb")
    fd.write(zf.read(name))
    print 'extracting', name
    fd.close()

localFile.close()
time.sleep(8)