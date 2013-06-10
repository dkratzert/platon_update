#/usr/bin/env python
#-*- encoding: utf-8 -*-
#möp
# this script updates the platon.exe in the c:\pwt directory

import urllib2
import os
import tempfile
import zipfile
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def main():
    html = urllib2.urlopen('http://www.cryst.chem.uu.nl/spek/xraysoft/update_history_platon.html')
    text = tempfile.TemporaryFile()
    text.write(html.read())
    text.close()
    print(dehtml(text))


main()

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