# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is the URL that is needed to query obituary database
# Page=2&countryid=1&daterange=Last3Days&stateid=57&keyword=&entriesperpage=50

import urllib2
import re
import pdb
import unicodedata
import csv

# pip install datefinder
import datefinder

# Beautiful soup object
from bs4 import BeautifulSoup

# Regular expression to get the name only from the text NOT WORKING RIGHT NOW
# name_extractor = re.compile('\b(?!Hello\b)\w+')


# A function that generates a URL to parse data given some parameters as required by db.
def generate_url(page_number, country, date_range, state_id, keyword, entries_per_page):
    # The base URL
    url_base = "http://www.legacy.com/ns/obitfinder/obituary-search.aspx?"
    # The uri parameters
    db_parameters = "Page=" + page_number + "&countryid=" + country + "&daterange=" + date_range + "&stateid=" + state_id +  "&keyword=" + keyword + "&entriesperpage=" + entries_per_page
    # Combine the two pieces to generate query URi
    url_with_parameters = url_base + db_parameters
    # Return the uri string
    return url_with_parameters


# A function to get dates from text courtesy of datefinder package.
def find_dates_on_text(text_to_analyze):
    found_dates = []
    matches = datefinder.find_dates(text_to_analyze)
    # Store them in empty array
    for date in matches:
        found_dates.append(name_string)
    # Spit them out
    return found_dates


# A function to request entries from the site.
def request_records(page_number, country, date_range, state_id, keyword, entries_per_page):
    # Attempt http connection
    try :
        # Open the needed URL
        web_page = urllib2.urlopen(generate_url(page_number, country, date_range, state_id, keyword, entries_per_page)).read()
        # This is an example: web_page = urllib2.urlopen(generate_url("1", "1", "Last3Days", "57", "", "50")).read()

        # Create an aray to store the names of the queried people
        parsed_names = []

        # Parsed people dictionary list FUTURE REFACTOR INTO HERE
        parsed_people = []

        # Soupify the text
        soup = BeautifulSoup(web_page, "html5lib")
        # Extract the name container of the person
        name_container = soup.findAll("div", { "class" : "obitName" })
        dob_container = soup.findAll("div", { "class" : "obitName" })
        # dod_container

        # Loop through the items - REFACTOR INTO STANDALONE FUNCTION
        for name in name_container:
            # Convert unicode into string to process and then downcase
            name_string = unicodedata.normalize('NFKD', name.a['title']).encode('ascii','ignore').lower()
            # Recover only the name of the person and only obituaries.
            # Check if the string contains an obituary
            if 'obituary' in name_string:
                # name_string = name_string.strip('read obituary for ')
                # Print the name just for debugging purposes
                print(name_string)
                # Append string to list of names
                parsed_names.append(name_string)

            # Remove the repeated elements

        # Return a list of names
        return parsed_names

    # Throw errors in case of HTTP errors
    except urllib2.HTTPError :
        print("HTTPERROR!")
    except urllib2.URLError :
        print("URLERROR!")


# A function to save the file.
def save_data_obtained(objects):
    # Do logic to save the CSV file
    with open('extracted_data.csv', 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = ["Name"], dialect='excel')
        writer.writeheader()
        writer.writerows({'Name' : parsed_names[row]} for row in range(0, len(parsed_names)))

# pdb.set_trace()

# Main request ====================================

parsed_names = request_records("1", "1", "Last3Days", "57", "", "50")
