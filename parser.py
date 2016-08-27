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
name_extractor = re.compile('(?:[a-z][a-z]+)\s+(?:[a-z][a-z]+)\s+(?:[a-z][a-z]+)\s', re.I)



# A function that generates a URL to parse data given some parameters as required by db.
# "2", "1", "Last3Days", "57", "", "50", "580"
def generate_url(page_number, date_range, affiliateid):
    # The base URL
    url_base = "http://www.legacy.com/ns/obitfinder/obituary-search.aspx?"
    # The uri parameters
    db_parameters = "Page=" + page_number + "&countryid=1" + "&daterange=" + date_range + "&stateid=57" + "&entriesperpage=50" + "&affiliateid=" + affiliateid
    # Combine the two pieces to generate query URi
    url_with_parameters = url_base + db_parameters
    # Return the uri string
    return url_with_parameters


# A function that generates a request and returns a soup object.
def generate_soup_from_uri(uri):
    try:
        # Execute the urlopen
        web_page = urllib2.urlopen(uri).read()
        # Use soup to convert to object
        soup = BeautifulSoup(web_page, "html5lib")
    # Throw errors in case of HTTP errors
    except urllib2.HTTPError :
        print("HTTPERROR!")
    except urllib2.URLError :
        print("URLERROR!")

    return soup


# A function to save data to a file.
def save_data_obtained(objects):
    # Do logic to save the CSV file
    with open('extracted_data.csv', 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = ["Name"], dialect='excel')
        writer.writeheader()
        writer.writerows({'Name' : objects[row]} for row in range(0, len(objects)))




# A function that gets the parameters that are going to be required in the extraction of data
def get_parameters_for_extraction(time_length, affiliate_code):
    # Get some soup from a uri, please refactor become input from user.
    soup = generate_soup_from_uri(generate_url("1", time_length, affiliate_code))
    # A dictionary that contains several parameters.
    extraction_session_params = {'number_of_pages' : 0, 'total_number_of_names' : 0, 'number_per_page' : 0}

    # The following header is where we have the key to all the parameters. It reads like this usually:  1 - 50 of 1000
    # First we get the div where the desired text is
    results_header_with_number_of_posts = soup.findAll("div", { "class" : "ResultsHeader" })
    # Now we get the important numbers inside the first <td>
    important_numbers = results_header_with_number_of_posts[0].find("td").findAll("b")
    # Convert unicode to integers
    first_item_in_page = int(important_numbers[0].text)
    last_item_in_page = int(important_numbers[1].text)
    number_of_items = int(important_numbers[2].text)

    # Calculate the number of pages with the formula floor((total_items)/last_item_in_page - first_item_in_page)
    calculated_number_of_pages = int(math.floor((number_of_items)/(last_item_in_page - first_item_in_page)))
    # Set the parameters for extraction session
    extraction_session_params['number_of_pages'] = calculated_number_of_pages
    extraction_session_params['number_per_page'] = int(((last_item_in_page)-(first_item_in_page)) + 1)
    extraction_session_params['total_number_of_names'] = number_of_items

    # Spit them parameters out!
    return extraction_session_params

# A function to look for the entries present on the page.
def request_obituaries(soup):
    # Look for the entries
    entry_containers = soup.findAll("div", { "class" : "entry" })
    # Empty list that will contain only the obituaries.
    obituaries = []
    for person in entry_containers:
        # Get the name from the title
        name_element = person.find("div", {"class" : "obitName"})
        # Convert to string the names in the title field for manipulation.
        name_string = unicodedata.normalize('NFKD', name_element.a['title']).encode('ascii','ignore').lower()
        # Only pass the obituaries.
        if 'obituary' in name_string:
            obituaries.append(person)

    return obituaries


# A function to request names from the queried site. ===========================
def request_name(person):
    # Extract the name container of the person
    name_container = person.find("div", { "class" : "obitName" })
    # Convert unicode into string to process and then downcase
    name_string = unicodedata.normalize('NFKD', name_container.a['title']).encode('ascii','ignore').lower()
    # Remove the initial string
    name_string = re.sub(r"(?:[a-z][a-z]+)\s+(?:[a-z][a-z]+)\s+(?:[a-z][a-z]+)\s", "", name_string)
    # Return the name
    return name_string
# ==================================================

# A function to get dates from text courtesy of datefinder package. ========================
def find_date_of_death(person):
    # Extract the container of text of the person
    text_container = person.find("div", { "class" : "obitText" })
    # Exctract the text of the found textfield
    date_containing_string = unicodedata.normalize('NFKD', text_container.text).encode('ascii','ignore')
    # Look inside the text of an entry for such words as, passed, died.
    try:
        death_finder = re.compile("(passed away.*|died.*)")
        death_text = death_finder.search(date_containing_string).group(1)
        # Use the datefinder library to look for dates on text
        matches = datefinder.find_dates(death_text)
        # Possible dates list
        possible_dates_of_death = []
        for match in matches:
            if not match:
                possible_dates_of_death[0] = "No date found"
            else:
                possible_dates_of_death.append(str(match))
            # Return the first date, which is most likely to be the correct one.
        return possible_dates_of_death[0]
    except:
        return "N/A"

# ============================================================================


# The main function that gets data needed, taking into account the number of pages ===============================
def execute_extraction():
    # Get input from the user about the desired length in time that is wanted
    print("Please input the length of time desired to go back in time to. Use Last3Days as an example")
    time_length = raw_input()

    print("Select the affiliate code, leave blank to choose all affiliates. Use 580 as example")
    affiliate_code = raw_input()
    if affiliate_code == "":
        affiliate_code == "580"

    # Get parameters for extraction, number of pages.
    params = get_parameters_for_extraction(time_length, affiliate_code)

    # Empty dictionary of people
    people_found = []

    # Go through each page and generate URLs for soupifying the data.
    for p in range(0, params['number_of_pages']):
        print("Extracting from page: " + str(int(p) + 1) + " out of " + str(params['number_of_pages']))
        # Page after page......
        # Generate a URL to query.
        url = generate_url(str(int(p)+1), time_length, affiliate_code)
        # Get the soup content from the URL generated.
        soup = generate_soup_from_uri(url)
        # Get the people in the page
        people = request_obituaries(soup)
        # For each person found
        for person in people:
            # Get the name
            name = request_name(person)
            # Get the dates of death
            date_of_death = find_date_of_death(person)
            # Get the date of birth
            # NOT YET IMPLEMENTED

            # Dictionary entry to add
            person_and_dates = {"name" : name, "death_date" : date_of_death}
            # Insert the person that was found into the list of dictionaries.
            people_found.append(person_and_dates)

    print(people_found)



# pdb.set_trace()

# Main request initiate ====================================
execute_extraction()
# parsed_names = request_records("2", "1", "Last3Days", "57", "", "50", "580")
# This is an example: "1", "1", "Last3Days", "57", "", "50", "580" | 580 for Dallas morning news
# Save the items
# save_data_obtained(parsed_names)
