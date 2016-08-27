# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is the URL that is needed to query obituary database
# Page=2&countryid=1&daterange=Last3Days&stateid=57&keyword=&entriesperpage=50

import urllib2
import re
import pdb
import unicodedata
import csv
import math

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

# A function that generates a request and returns a soup object.
def generate_soup_from_uri(uri):
    # Execute the urlopen
    web_page = urllib2.urlopen(uri).read()
    # Use soup to convert to object
    soup = BeautifulSoup(web_page, "html5lib")
    return soup


# A function to get dates from text courtesy of datefinder package.
# def find_dates_on_text(text_to_analyze):
#     found_dates = []
#     matches = datefinder.find_dates(text_to_analyze)
#     # Store them in empty array
#     for date in matches:
#         found_dates.append(name_string)
#     # Spit them out
#     return found_dates



# A function that gets the parameters that are going to be required in the extraction of data
def get_parameters_for_extraction():
    # Get input from the user about the desired length in time that is wanted
    print("Please input the length of time desired to go back in time to. Use Last3Days as an example")
    time_length = raw_input()

    # Get some soup from a uri, please refactor become input from user.
    soup = generate_soup_from_uri(generate_url("1", "1", time_length, "57", "", "50", "580"))
    # A dictionary that contains several parameters.
    extraction_session_params = {'number_of_pages' : 0, 'total_number_of_names' : 0, 'number_per_page' : 0}
    # The following header is where we have the key to all the parameters. It reads like this usually:  1 - 50 of 1000
    pdb.set_trace()
    # First we get the div where the desired text is
    results_header_with_number_of_posts = soup.findAll("div", { "class" : "ResultsHeader" })
    # Now we get the important numbers inside the first <td>
    important_numbers = results_header_with_number_of_posts[0].find("td").findAll("b")
    # Convert unicode to integers
    first_item_in_page = int(important_numbers[0].text)
    last_item_in_page = int(important_numbers[1].text)
    number_of_items = int(important_numbers[2].text)

    # Set the parameters for extraction session

    # Calculate the number of pages with the formula floor((total_items)/last_item_in_page - first_item_in_page)
    calculated_number_of_pages = int(math.floor((number_of_items)/(last_item_in_page - first_item_in_page)))

    extraction_session_params['number_of_pages'] = calculated_number_of_pages
    extraction_session_params['number_per_page'] = int(((last_item_in_page)-(first_item_in_page)) + 1)
    extraction_session_params['total_number_of_names'] = number_of_items

    return extraction_session_params


# A function that gets data needed, taking into account the number of pages


# A function to implement the number of pages that need to be navigated to extract data from.
# def get_number_of_pages(webpage_soup_object):
#     pagination_container = webpage_soup_object.findAll("div", { "id" : "Pagination" }).span.a
#     return len(pagination_container)

# A function that gets records from a specific page number
# def get_paged_records(page_number):
#     # Soupified Paged Elements
#     paged_elements = ""
#     return paged_elements


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

# parsed_names = request_records("2", "1", "Last3Days", "57", "", "50", "580")
# This is an example: "1", "1", "Last3Days", "57", "", "50", "580" | 580 for Dallas morning news
# Save the items
# save_data_obtained(parsed_names)

get_parameters_for_extraction()
