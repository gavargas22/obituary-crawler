# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

# Get input from the user
# The state is chosen by default
# desired_state = raw_input('Enter a State name: ')
state_to_query_state = 57



# This is the URL that is needed to query obituary database
# Page=2&countryid=1&daterange=Last3Days&stateid=57&keyword=&entriesperpage=50


try :
    web_page = urllib2.urlopen("http://www.legacy.com/ns/obitfinder/obituary-search.aspx?" + "Page=" + 1 + "&countryid="1&daterange=Last3Days&stateid=57&keyword=&entriesperpage=50").read()
    soup = BeautifulSoup(web_page, "html5lib")
    # specific_content_object = soup.find('status', {'class':'vi'}).contents
    specific_content_object = soup.find('status').contents
    print(specific_content_object)
except urllib2.HTTPError :
    print("HTTPERROR!")
except urllib2.URLError :
    print("URLERROR!")

# A function that generates a URL to parse data given some parameters as required by db.
def generate_url(page_number, country, date_range, state_id, keyword, entries_per_page):
    # The base URL
    url_base = "http://www.legacy.com/ns/obitfinder/obituary-search.aspx?"
    db_parameters = "?Page=" + page_number + "&countryid=" + country + "&daterange=" + daterange + "&stateid=" + state_id +  "&keyword=" + keyword + "&entriesperpage=" + entries_per_page
    # Combine the two pieces to query URL
    url_with_parameters = url_base + db_parameters
    # Return the string
    return url_with_parameters
