# speedrun.com data collection project

> this project implements a selenium based webscraper to collect leaderboard data from speedrun.com

## initialising the scraper and navigating the site

- a file 'scraper.py' is created in the folder './srdotcomScraper' in which we define the 'Scraper()' class

- the package 'selenium' is used to open an automated firefox browser window. the private method '_load_site()' also accepts cookies.

```python
    myScraper = Scraper('speedrun.com')
```

- the 'search(query)' method allows the user to find a game of their choice using
  
```python
    myScraper.search('<name of game>')
```

- the 'next_cat()' method allows the user to cycle through each category for the game being viewed, including miscellaneous categories. this method returns 'True' when returning to the initial category and 'False' in any other situation. this can be used to break a loop cycling through all categories.

```python
    done = myScraper.next_cat()
```

## scraping the data

- the 'get_all_cat_PBs()' method is implemented to find the information for every run on the leaderboard (not including obsolete runs). it stores the runner name, time and vod link (if there is one) along with a unique uuid string for identification purposes in a dictionary format.

```python
    catDict = get_all_cat_PBs()
```

- this method is used by the broader method 'get_all_game_PBs()', which uses 'next_cat()' to cycle through each category for a game and 'get_all_cat_PBs()' to get the times for each category. this data is then stored in a dictionary with the structure

```python
    gameDict = {'game_id': re.split('#',self.driver.current_url[25:])[0], 'game_uuid': str(uuid.uuid4()), 'category': []}
```

- where 'game_id' uses regex to take only the name of the game from the url (which is formatted like 'https://www.speedrun.com/spyro1#120'), 'game_uuid' is another uuid string and 'category' is a list that contains a readable id for each category, a uuid each the category, a link to each category and the data for each category provided by 'get_all_cat_PBs()'

- this larger dictionary can then be saved to a json file with the name format game_id.json

## testing

- a testing suite is created and stored in the file 'test_scraper.py' in the folder './test'. this is file contains unit tests for each method within the 'Scraper()' class