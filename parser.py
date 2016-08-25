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


# A function that generates a URL to parse data given some parameters as required by db. MAY NOT BE USED AFTER ALL
def generate_url(page_number, country, date_range, state_id, keyword, entries_per_page, affiliateid):
    # The base URL
    url_base = "http://www.legacy.com/ns/obitfinder/obituary-search.aspx?"
    # The uri parameters
    db_parameters = "Page=" + page_number + "&countryid=" + country + "&daterange=" + date_range + "&stateid=" + state_id +  "&keyword=" + keyword + "&entriesperpage=" + entries_per_page + "&affiliateid=" + affiliateid
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


# A function to implement the number of pages that need to be navigated to extract data from.
def get_number_of_pages(webpage_soup_object):
    pagination_container = webpage_soup_object.findAll("div", { "id" : "Pagination" }).span.a
    return len(pagination_container)

# A function that gets records from a specific page number
def get_paged_records(page_number):
    # Soupified Paged Elements
    paged_elements = ""
    return paged_elements

# A function to request entries from the site.
def request_records(page_number, country, date_range, state_id, keyword, entries_per_page, affiliateid):
    # Attempt http connection
    try :
        # Open the needed URL
        # web_page = urllib2.urlopen(url_with_parameters).read()
        web_page = urllib2.urlopen(generate_url("1", "1", "Last3Days", "57", "", "50", "580")).read()
        # This is an example: web_page = urllib2.urlopen(generate_url("1", "1", "Last3Days", "57", "", "50")).read()

        # Soupify the site
        soup = BeautifulSoup(web_page, "html5lib")

        # Get the number of pages needed to check
        # number_of_pages = get_number_of_pages(soup)

        # Create an aray to store the names of the queried people
        parsed_names = []

        # Parsed people dictionary list FUTURE REFACTOR INTO HERE
        parsed_people = []

        # Extract the name container of the person
        name_container = soup.findAll("div", { "class" : "obitName" })

        # Date of birth items
        dob_container = soup.findAll("div", { "class" : "obitName" })

        # Date of death items
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
        writer.writerows({'Name' : objects[row]} for row in range(0, len(objects)))

# pdb.set_trace()

# Main request initiate ====================================

parsed_names = request_records("1", "1", "Last3Days", "57", "", "50", "580")
# This is an example: "1", "1", "Last3Days", "57", "", "50", "580" | 580 for Dallas morning news
# Save the items
save_data_obtained(parsed_names)
