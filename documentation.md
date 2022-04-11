# DATA COLLECTION PIPELINE

Aims: use a webscraper to take leaderboard info from speedrun.com and format the data

------------------[PACKAGES USED]------------------



------------------[THE SCRAPER CLASS]------------------

- the scraper class can be called using myScraper = scraper(URL)

------------------[METHODS]------------------

- __init__(URL)
    - initialises selenium webdriver and stores a given URL

- load_site()
    - opens the URL provided when scraper class is called and accepts cookies

- search(query)
    - performs a search for 'query' in the speedrun.com search bar and navigates to the first result shown

- nextCat()
    - navigates to next category for current game
        - eg if the current url is 'speedrun.com/spyro1#any', calling nextCat() will navigate to 'speedrun.com/spyro1#120'
    - if on last category will navigate back to first category
        - returns boolean 'done = True' when this happens
        - else returns 'done = False'. this can be used to break a loop eg in getCatLinks()

- getCatLinks()
    - collects links to all categories for current game
    - requires current page to be the first category
    - returns links to all categories as a list

- getAllCatPBs()
    - gets all PBs for the category being viewed (i.e. all times on the leaderboard)
    - returns lists of runner names, times and links to vods
        - if a run has no vod available, returns None for that list element4