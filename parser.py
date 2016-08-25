# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib2
import re
import pdb
import unicodedata
import csv


from bs4 import BeautifulSoup
# Regular expression to get the name only from the text
name_extractor = re.compile('\b(?!Hello\b)\w+')
# Get input from the user
# The state is chosen by default
# desired_state = raw_input('Enter a State name: ')
state_to_query_state = 57

# A function that generates a URL to parse data given some parameters as required by db.
def generate_url(page_number, country, date_range, state_id, keyword, entries_per_page):
    # The base URL
    url_base = "http://www.legacy.com/ns/obitfinder/obituary-search.aspx?"
    db_parameters = "Page=" + page_number + "&countryid=" + country + "&daterange=" + date_range + "&stateid=" + state_id +  "&keyword=" + keyword + "&entriesperpage=" + entries_per_page
    # Combine the two pieces to query URL
    url_with_parameters = url_base + db_parameters
    # Return the string
    return url_with_parameters


# This is the URL that is needed to query obituary database
# Page=2&countryid=1&daterange=Last3Days&stateid=57&keyword=&entriesperpage=50

# A function to request entries from the site.
def request_records(page_number, country, date_range, state_id, keyword, entries_per_page):
    try :
        # Create an aray to store the names of the queried people
        parsed_names = []
        # Open the needed URL
        web_page = urllib2.urlopen(generate_url(page_number, country, date_range, state_id, keyword, entries_per_page)).read()
        # This is an example: web_page = urllib2.urlopen(generate_url("1", "1", "Last3Days", "57", "", "50")).read()
        # Soupify the text
        soup = BeautifulSoup(web_page, "html5lib")
        # Extract the name container of the person
        name_container = soup.findAll("div", { "class" : "obitName" })

        # Loop through the items
        for name in name_container:
            # Convert unicode into string to process and then downcase
            name_string = unicodedata.normalize('NFKD', name.a['title']).encode('ascii','ignore').lower()
            # Recover only the name of the person and only obituaries.
            # Check if the string contains an obituary
            if 'obituary' in name_string:
                name_string = name_string.strip('read obituary for ')
                # Print the name just for debuggin purposes
                print(name_string)
                # Append string to array of names
                parsed_names.append(name_string)
        # Return a list
        return parsed_names

    except urllib2.HTTPError :
        print("HTTPERROR!")
    except urllib2.URLError :
        print("URLERROR!")


pdb.set_trace()
parsed_names = request_records("1", "1", "Last3Days", "57", "", "50")
pdb.set_trace()
with open('extracted_data.csv', 'w+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = ["Name"], dialect='excel')
    writer.writeheader()
    writer.writerows({'Name' : parsed_names[row]} for row in range(0, len(parsed_names)))
