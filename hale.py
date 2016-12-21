# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 08:01:42 2016



<div class="select-wrapper"><!--
  --><select name="js_dropdown" class="js-dropdown">

     <option value="/menu/?location=17th-and-broadway"
             selected="selected"
             >17th &amp; Broadway</option>

https://www.haleandhearty.com/menu/?location=

@author: gfrazier
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
        soup = BeautifulSoup(html.text, "html.parser")
        return soup

def get_locations(soup):

    locs = soup.select('option[value^="/menu/?location="]')
    n = len(locs)
    #value iterable from BS4
    locations = [value['value'] for value in locs]
    #print (locations, names)
    return locations

def get_names(soup):
    #extract option tag with value="matching string"
    storeid = soup.find(id="our-menu").find_all('option')
    n = len(storeid)
    names = [storeid[i].text for i in range(n)]
    return names

def get_menu_items(soup):

    #menu = soup.select("menu-item__name")
    items = soup.find_all(class_="menu-item__name") #has tags
    prices = soup.find_all(class_="menu-item__price") #has tags
    n = len(items)

    item_name = [items[i].text for i in range(n)]
    item_price = [prices[i].text for i in range(n)]
    strprice = [item_price[i].strip() for i in range(n)] #strip newlines
    justprice = [strprice[i].strip('\n\n+') for i in range(n)] #remove extra /n bits
    menu_items = dict(zip(item_name, justprice)) #zip into dict with item:price
    return menu_items

def form_url(site, loc):

    url = site + loc

    return url

def write_menu(date, sname, name, menu, path, file):
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
    #soup = extract_soup(html)
    locations = get_locations(soup)
    names = get_names(soup)
    for i in locations:
        # loc = (value['value']) #value iterable from BS4
        #loc= ['17th-and-broadway'] #single loc for testing
        url = form_url(site, loc) #list value for testing
        soup = get_soup(url)
        sname = loc[i].strip(r'/menu/?location=')
        name = names[i]
        menu = get_menu_items(soup) #return dictionary
        write_menu(date, sname, name, menu, path, 'day-menu.csv')
        mcount = len(menu)
        print('Store {} has a menu of {} items.'.format(name, mcount))
if __name__ == "__main__":
    main()
