#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# This script updates the platon.exe in the c:\pwt directory.
pyver = 2
try:
    import urllib2
except ModuleNotFoundError:
    import urllib.request
    pyver = 3
import os
import sys
import time
import tempfile
import zipfile
if pyver == 2:
    from HTMLParser import HTMLParser
if pyver == 3:
    from html.parser import HTMLParser
import datetime
changes_url = 'http://www.platonsoft.nl/spek/xraysoft/update_history_platon.html'
platon_url = 'http://www.platonsoft.nl/spek/xraysoft/mswindows/platon/platon.zip'

# fetch the changes of platon and store it in one string (text)
if pyver == 2:
    htmlp = urllib2.urlopen(changes_url)
    text = [htmlp.next() for x in range(25)]
    text = "".join(text)
if pyver == 3:
    with urllib.request.urlopen(changes_url) as f:
        text = [x.decode('utf-8') for x in f.readlines()]
    text = "".join(text[:25])
else:
    print("Unable to download platon. Use Python2 or 3.")


#strips down the html to plain text
class MLStripper(HTMLParser):
    def __init__(self):
        if pyver == 3:
            super().__init__()
        self.reset()
        self.fed = []
        
    def handle_data(self, d):
        self.fed.append(d.rstrip('\n'))
        
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(htmlp):
    s = MLStripper()
    s.feed(htmlp)
    return s.get_data()

today = datetime.date.today()
print("\nToday is: {}".format(str(today.strftime('%b %d, %Y\n'))))
print(strip_tags(text))
    

# now preceed with platon update
if pyver == 2:
    u = urllib2.urlopen(platon_url)
    data = u.read()
if pyver == 3:
    req = urllib.request.Request(platon_url)
    with urllib.request.urlopen(req) as response:
        data = response.read()

#create a temporary file and download platon to it.
localFile = tempfile.TemporaryFile()
localFile.write(data)

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
        print("unable to create install directory")
        sys.exit()
    else:
        print('created platon directory c:\\pwt')
        pass
# extract the files to the platon directory
for name in list:
    fd = open('c:/pwt/'+name, "wb")
    fd.write(zf.read(name))
    print('extracting {}'.format(name))
    fd.close()

localFile.close()
time.sleep(10)