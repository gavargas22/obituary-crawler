# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

try :
    web_page = urllib2.urlopen("http://skunkworks.at.utep.edu/skunk/doors/1/status").read()
    soup = BeautifulSoup(web_page, "html5lib")
    # specific_content_object = soup.find('status', {'class':'vi'}).contents
    specific_content_object = soup.find('status').contents
    print(specific_content_object)
except urllib2.HTTPError :
    print("HTTPERROR!")
except urllib2.URLError :
    print("URLERROR!")
