## Flow for hale.py

URL is set  

config data (part of main?)  
    set up namedtuple  
    unzip and unpickle datafile  
    return datafile and namedtuple  

get soup  
get HTML using requests  
HTML to BeautifulSoup parser

get locations  
pull out the location specific URLS from option value

get names  
pull out location names from options  

roll through the location pages  
get soup  
  get menu items  
  parse menu  
    clean  
        is new item?  
             
            yes add item data  
                parse tags  
                parse ingredients  
                parse calories  
                parse nutrition facts (optional?)
                add first date  
                  
            no pass  
        parse price  
            clean  
        zip into dictionary  
    write menu to csv  
repickle and rezip datafile  