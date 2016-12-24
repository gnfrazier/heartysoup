## Flow for hale.py

URL is set

get soup
    - get HTML using requests
    - HTML to BeautifulSoup parser

get locations
    - pull out the location specific URLS from option value

get names
    - pull out location names from options

roll through the location pages
    - get soup
    get menu items
        - parse menu
            - clean
        - is new item?
            unzip and unpickle datafile
            - yes add item data
                parse tags
                parse ingredients
                parse calories
                parse nutrition facts (optional?)
                add first date
                repickle and rezip datafile

            - no pass
        - parse price
            - clean
        - zip into dictionary

    write menu to csv
