## Flow for hale.py

URL is set
get locations
    get soup
        -get HTML using requests
        -HTML to BeautifulSoup parser
    -pull out the location specific URLS from option value

-roll through the location pages
    get menu items  
        -get soup

        -parse menu
            -clean
        -parse price
            -clean
        -zip into dictionary

    write menu to csv
