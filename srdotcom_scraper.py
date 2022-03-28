from xmlrpc.client import boolean
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import uuid
import requests
import time
import json
import typing as t

class scraper:

    '''
    This class acts as a web scraper for speedrun.com.

    The scraper is able to search for a game and collect the leaderboard data for every main and miscellaneous category, saving it in a json format.

    Attributes:
        URL (str): the initial URL for the webdriver, defaults to https://www.speedrun.com 
    '''

    def __init__(self,URL: str = 'https://www.speedrun.com'):
        self.URL = URL
        self.driver = webdriver.Firefox()
        self._load_site()

    def _load_site(self) -> webdriver.Firefox:
        '''
        Loads site and accepts cookies (on sr.com)
        '''
        self.driver.get(self.URL)
        try:
            accept_cookies_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="fc-button fc-cta-consent fc-primary-button"]')))
            accept_cookies_button.click()
            print('[INFO] cookies accepted')
            time.sleep(1)
        except TimeoutException:
            print('[ERROR] timeout exception when trying to accept cookies')

    
    # TO DO: -FIGURE OUT HOW TO SEARCH ONLY THE GAMES LIST, IGNORING THE SERIES LIST
    #        -MAYBE IMPLEMENT searchGame AND searchUser AS SEPARATE FUNCTIONS
    
    def search(self,query: str):
        '''
        Searches for 'query' in the search bar and chooses the first result

        Args:
            query (str): the query to be searched
        '''
        search_bar = self.driver.find_element(by=By.XPATH, value='//*[@type="search"]')
        search_bar.click()
        time.sleep(0.5)
        search_bar.send_keys(query)
        try:
            result = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="ui-menu-item"]')))
            result.click()
            print(f'[INFO] redirected to {self.driver.current_url}')
            time.sleep(0.5)
        except:
            print('[ERROR] no results found')
        

    def get_all_cat_PBs(self):
        '''
        Collects all the times on the leaderboard for selected category (i.e. PBs of all players with runs on the board) + name of runner + link to VOD

        Returns:
            dict: a dictionary with info for all PBs for selected category
        '''
        all_runs = self.driver.find_element(by=By.XPATH, value='//table[@id="primary-leaderboard"]')
        names = all_runs.find_elements(by=By.XPATH, value='//span[@class="nobr" or @class="username"]')
        times = all_runs.find_elements(by=By.XPATH, value='//tr/td[@class="nobr center hidden-xs"][1]')
        vods = all_runs.find_elements(by=By.XPATH, value='//tr/td[@class="run-video nobr center hidden-xs hidden-md-down"]')
        cat_dict = {'runs': []}
        for i in range(len(times)):
            try:
                vod_div = vods[i].find_element(by=By.TAG_NAME, value='a')
                vod_link = vod_div.get_attribute("href")
            except:
                vod_link = None
            cat_dict['runs'].append({'time': times[i].text, 'name': names[i].text, 'vod': vod_link})
        return cat_dict


    def next_cat(self) -> t.Optional[bool]:
        '''
        Switches page to next category. If on last category, returns to the initial category.

        Returns:
            bool: True if returning to initial category.
        '''
        done = False
        try:
            misc_button = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab active"]/following-sibling::a[1][@id="miscellaneous"]')
            misc_button.click()
            next_category = self.driver.find_element(by=By.XPATH, value='//a[@class="dropdown-item category"]')
        except:    # myScraper.load_site()
                try:
                    misc_button = self.driver.find_element(by=By.XPATH, value='//a[@id="miscellaneous"]')
                    misc_button.click()
                    next_category = self.driver.find_element(by=By.XPATH, value='//a[@class="dropdown-item category active"]/following-sibling::a')
                except:
                    next_category = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab"]')
                    done = True
        next_category.click()
        time.sleep(0.5)
        return done # Use this to break a loop cycling through all categories


    def get_all_game_PBs(self) -> dict:
        '''
        Gets PBs for all categories for game with links and IDs for each category, stores this info in a dictionary.

        Returns:
            dict: a dictionary with info for all PBs for selected game
        '''
        game_dict = {'category': []}
        done = False
        while done == False:
            done = self.next_cat()
            cat_dict = self.get_all_cat_PBs()
            game_dict['category'].append({'id': self.driver.current_url[25:], 'uuid': str(uuid.uuid4()), 'link': self.driver.current_url, 'runs': cat_dict})
        return game_dict
            


if __name__ == "__main__":
    myScraper = scraper()
    myScraper.search('Spyro the dragon')
    game_id = myScraper.driver.current_url[25:]
    my_dict = myScraper.get_all_game_PBs()

    with open(game_id+'_PBs.json', mode='w') as f:
        json.dump(my_dict, f)

    myScraper.driver.quit()
