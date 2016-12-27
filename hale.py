# -*- coding: utf-8 -*-
"""
Scrape the menu from Hale and Hearty Soups website for fun on a cold winter day.

Outputs the day's menu by location with prices.
"""

import requests
from bs4 import BeautifulSoup
import arrow
import time
from collections import namedtuple
import csv
import os
import string


def get_soup(url):
    """Check for a 200 response from the website and return parsed soup object."""

    html = requests.get(url)

    if html.status_code == 200:
        # soup = BeautifulSoup(html.text, "html.parser") #changed to own
        # function
        soup = extract_soup(html)
        return soup
    else:
        response = html.status_code
        print('{} returned a {} status code.'.format(url, response))
        return none


def extract_soup(html):
    """Extract the soup object from the passed HTML."""

    soup = BeautifulSoup(html.text, "html.parser")
    return soup


def get_locations(soup):
    """Return a list of store location URL parameters."""

    # extract option tag with value="matching string"
    locs = soup.select('option[value^="/menu/?location="]')
    n = len(locs)
    # value iterable from BS4
    locations = [value['value'] for value in locs]
    #print (locations, names)
    return locations


def get_names(soup):
    """Return a list of store location public names"""

    storeid = soup.find(id="our-menu").find_all('option')
    n = len(storeid)
    names = [storeid[i].text for i in range(n)]
    return names


def get_menu_items(soup):
    """Return a dictionary of key menu-items and value prices"""

    items = clean(soup.find_all(class_="menu-item__name"))  # has tags
    prices = clean(soup.find_all(class_="menu-item__price"))  # has tags

    menu_items = dict(zip(items, prices))  # zip into dict with item:price
    return menu_items


def add_new_items(soup):
    info = soup.find_all(class_="md-info")
    archive = get_archive()
    first = date()
    details = namedtuple(
        'details', "name, desc, cal, ingred, tag, fact, first")
    for item in info:
        # extract and clean the name
        name = cleana(item.find(class_="md-name"))
        # check if new
        if name not in archive:
            # if new build tuple of attributes
            desc = cleana(item.find(class_="menu-item__desc"))
            cal = cleana(item.find(class_="menu-item__cals"))
            ingred = cleana(item.find(class_="menu-item__ingredients"))
            tag = cleana(item.find(class_="menu-item__tags"))
            fact = cleana(item.find(class_="menu-item__nutrition-facts"))

            detail = details(name, desc, cal, ingred, tag, fact, first)
            archive[name] = detail

            write_archive(archive)

    return archive


def clean(tagged):
    """clean tags and new lines out of list of attributes"""

    n = len(tagged)
    untagged = [tagged[i].text for i in range(n)]  # strip tags
    stripped = [untagged[i].strip() for i in range(n)]  # strip newlines
    nolines = [stripped[i].strip('\n\n+')
               for i in range(n)]  # rm extra /n bits

    return nolines


def cleana(tagged):
    """clean tags and new lines out of single attribute"""
    if tagged:
        untagged = (tagged.text)  # strip tags
        stripped = (untagged.strip())  # strip newlines
        nolines = (stripped.strip('\n\n+'))  # rm extra /n bits
    else:
        nolines = "None"
    return nolines


def form_url(site, loc):
    """Concatenate site URI with location specific parameters"""

    url = site + loc

    return url


def write_menu(date, sname, name, menu, path, file):
    """Append data to output file passed as path, file"""

    file_name = path + file
    with open(file_name, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        for item, price in menu.items():
            line = (date, sname, name, item, price)
            writer.writerow(line)


def get_archive():
    """Opens the existing datafile and returns it as dictionary"""

    try:
        with open('itemfile.json')as infile:
            archive = json.load(infile)
    except:
        archive = {}
    return archive


def write_archive(archive):
    """Writes updated archive dict to datafile in json format"""

    with open('itemfile.json', 'a')as outfile:
        json.dump(archive, outfile)


def date():
    date = arrow.now('US/Eastern').format('YYYY-MM-DD')
    return date


def main():
    path = os.getcwd() + '/'
    date = date()
    site = 'https://www.haleandhearty.com'
    soup = get_soup(site)
    locations = get_locations(soup)
    names = get_names(soup)

    for i in range(len(locations)):
        """Iterate through locations list, append menu to output file."""

        loc = locations[i]
        url = form_url(site, loc)
        soup = get_soup(url)
        sname = loc.strip(r'/menu/?location=')
        name = names[i]
        menu = get_menu_items(soup)  # return dictionary
        write_menu(date, sname, name, menu, path, 'day-menu.csv')
        add_new_items(soup)
        mcount = len(menu)
        print('Store {} has a menu of {} items.'.format(name, mcount))


if __name__ == "__main__":

    main()
