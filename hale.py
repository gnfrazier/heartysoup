#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Scrape the menu from Hale and Hearty Soups website on a cold winter day.

Outputs the day's menu by location with prices.
"""

import requests
from bs4 import BeautifulSoup
import arrow
import csv
import os
import tablib


def get_soup(url):
    """Check for a 200 response from the website and return soup object."""

    html = requests.get(url)

    if html.status_code == 200:
        soup = extract_soup(html)
        return soup

    else:
        response = html.status_code
        print('{} returned a {} status code.'.format(url, response))
        return None


def extract_soup(html):
    """Extract the soup object from the passed HTML."""

    soup = BeautifulSoup(html.text, "html.parser")
    return soup


def get_locations(soup):
    """Return a list of store location URL parameters."""

    # extract option tag with value="matching string"
    locs = soup.select('option[value^="/menu/?location="]')
    # value iterable from BS4
    locations = [value['value'] for value in locs]
    # print (locations, names)
    return locations


def new_get_locations(soup):
    store = soup.find_all(class_="locations-list__location")
    locations = []
    for location in store:
        loc = str(location)
        locsoup = BeautifulSoup(loc, "html.parser")

        for link in locsoup.find_all('a'):
            url = link.get('href')
            locations.append(url)
    return locations


def get_names(soup):
    """Return a list of store location public names"""

    storeid = soup.find(id="our-menu").find_all('option')
    n = len(storeid)
    names = [storeid[i].text for i in range(n)]
    return names


def new_get_names(soup):
    store = soup.find_all(class_="locations-list__location")
    names = []
    for location in store:
        name = extract_soup(location)
        names.append(name)
    return clean(names)


def get_menu_items(soup):
    """Return a dictionary of key menu-items and value prices"""

    items = clean(soup.find_all(class_="menu-item__name"))  # has tags
    prices = clean(soup.find_all(class_="menu-item__price"))  # has tags

    menu_items = dict(zip(items, prices))  # zip into dict with item:price
    return menu_items


def add_new_items(soup):
    info = soup.find_all(class_="md-info")
    itemlist = read_itemfile()
    first = date()
    for item in info:
        # extract and clean the name
        name = cleana(item.find(class_="md-name"))
        namelist = itemlist['Name']
        # check if new
        if name not in namelist:

            # if new add attributes to itemfile
            desc = cleana(item.find(class_="menu-item__desc"))
            cal = cleana(item.find(class_="menu-item__cals"))
            ingred = cleana(item.find(class_="menu-item__ingredients"))
            tag = cleana(item.find(class_="menu-item__tags"))
            fact = cleana(item.find(class_="menu-item__nutrition-facts"))

            itemlist.append([name, desc, cal, ingred, tag, fact, first])
            print('Item added')
            print(len(itemlist))
    write_itemfile(itemlist)

    return itemlist


def clean(tagged):
    """clean tags and new lines out of list of attributes"""

    n = len(tagged)
    # strip tags
    untagged = [tagged[i].text for i in range(n)]

    # replace newlines with space
    stripped = [untagged[i]
                .replace('\n\n+', ' ')
                .replace('\n', ' ')
                .replace('\r', ' ')
                for i in range(n)]

    # strip trailing spaces
    nolines = [stripped[i].strip() for i in range(n)]
    return nolines


def cleana(tagged):
    """clean tags and new lines out of single attribute"""

    if tagged:
        untagged = (tagged.text)  # strip tags
        # strip newlines
        stripped = (untagged
                    .replace('\n\n+', ' ')
                    .replace('\n', ' ')
                    .replace('\r', ' '))
        nolines = (stripped.strip())  # strip trailing spaces

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


def read_itemfile():
    """Open existing itemlist and return as tablib data object"""

    try:
        itemlist = tablib.Dataset().load(open('itemfile.csv').read())
    except:
        itemlist = setup_itemfile()
        print('Unable to read itemfile. Creating new itemfile')

    return itemlist


def write_itemfile(itemlist):
    """Write data file as .csv"""

    try:
        with open('itemfile.csv', 'w') as f:
            f.write(itemlist.csv)
        return True
    except:
        return False


def setup_itemfile():
    """Only if itemlist.csv can not be opened, set up new itemlist"""

    itemlist = tablib.Dataset()
    itemlist.headers = ['Name', 'Description', 'Calories',
                        'Ingredients', 'Tags', 'Nutrition Facts',
                        'First Recorded']

    return itemlist


def date():
    date = arrow.now('US/Eastern').format('YYYY-MM-DD')
    return date


def main():
    path = os.getcwd() + '/'
    today = date()
    site = 'https://www.haleandhearty.com'
    home = '/locations/#main'
    url = form_url(site, home)
    soup = get_soup(url)
    locations = new_get_locations(soup)
    names = new_get_names(soup)

    for i in range(len(locations)):
        """Iterate through locations list, append menu to output file."""

        loc = locations[i]
        url = form_url(site, loc)
        soup = get_soup(url)
        sname = loc.strip(r'/menu/?location=')
        name = names[i]
        menu = get_menu_items(soup)  # return dictionary
        write_menu(today, sname, name, menu, path, 'day-menu.csv')
        add_new_items(soup)
        mcount = len(menu)
        print('Store {} has a menu of {} items.'.format(name, mcount))


if __name__ == "__main__":

    main()
