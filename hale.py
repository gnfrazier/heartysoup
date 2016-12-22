# -*- coding: utf-8 -*-
"""
Scrape the menu from Hale and Hearty Soups website for fun on a cold winter day.

Outputs the day's menu by location with prices.
"""

import requests
from bs4 import BeautifulSoup
import arrow
import time
import collections
import csv
import os
import string

def get_soup(url):
    """Check for a 200 response from the website and return parsed soup object."""

    html = requests.get(url)

    if html.status_code == 200:
        # soup = BeautifulSoup(html.text, "html.parser") #changed to own function
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

    #extract option tag with value="matching string"
    locs = soup.select('option[value^="/menu/?location="]')
    n = len(locs)
    #value iterable from BS4
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

    items = soup.find_all(class_="menu-item__name") #has tags
    prices = soup.find_all(class_="menu-item__price") #has tags
    n = len(items)

    item_name = [items[i].text for i in range(n)] #removes tags
    item_price = [prices[i].text for i in range(n)] #removes tags
    strname = [item_name[i].strip() for i in range(n)] #strip newlines
    strprice = [item_price[i].strip() for i in range(n)] #strip newlines
    justprice = [strprice[i].strip('\n\n+') for i in range(n)] #remove extra /n bits
    menu_items = dict(zip(strname, justprice)) #zip into dict with item:price
    return menu_items

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

def main():
    path = os.getcwd() + '/'
    date = arrow.now('US/Eastern').format('YYYY-MM-DD')
    site = 'https://www.haleandhearty.com'
    soup = get_soup(site)
    locations = get_locations(soup)
    names = get_names(soup)

    for i in range(len(locations)):
        """Iterate through locations list, append menu to output file."""
        
        loc = locations[i]
        url = form_url(site, loc) #list value for testing
        soup = get_soup(url)
        sname = loc.strip(r'/menu/?location=')
        name = names[i]
        menu = get_menu_items(soup) #return dictionary
        write_menu(date, sname, name, menu, path, 'day-menu.csv')
        mcount = len(menu)
        print('Store {} has a menu of {} items.'.format(name, mcount))


if __name__ == "__main__":

    main()
