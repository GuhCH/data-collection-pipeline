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
import re
import datetime as dt



class Scraper:

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
        self.driver.maximize_window()
        try:
            accept_cookies_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="fc-button fc-cta-consent fc-primary-button"]')))
            accept_cookies_button.click()
            print('[INFO] cookies accepted')
            time.sleep(1)
        except TimeoutException:
            print('[ERROR] timeout exception when trying to accept cookies')

    
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
            result = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="dropdown-header ui-autocomplete-category"][text()="Games"]/following-sibling::li[1]')))
            result.click()
            print(f'[INFO] redirected to {self.driver.current_url}')
            time.sleep(0.5)
        except:
            print('[ERROR] no results found')


    def get_all_cat_PBs(self):
        '''
        Collects all the times on the leaderboard for selected category (i.e. PBs of all players with runs on the board) in ISO format + name of runner + link to VOD

        Returns:
            dict: a dictionary with info for all PBs for selected category
        '''
        all_runs = self.driver.find_element(by=By.XPATH, value='//table[@id="primary-leaderboard"]')
        names = all_runs.find_elements(by=By.XPATH, value='//span[@class="nobr" or @class="username"]')
        times = all_runs.find_elements(by=By.XPATH, value='//tr/td[@class="nobr center hidden-xs"][1]')
        vods = all_runs.find_elements(by=By.XPATH, value='//tr/td[@class="run-video nobr center hidden-xs hidden-md-down"]')
        dtoptions = ['%Hh %Mm %Ss %fms','%Mm %Ss %fms', '%Ss %fms','%fms','%Hh %Mm %Ss','%Mm %Ss','%Ss']
        cat_dict = {'runs': []}
        for i in range(len(times)):
            try:
                vod_div = vods[i].find_element(by=By.TAG_NAME, value='a')
                vod_link = vod_div.get_attribute("href")
            except:
                vod_link = None
            for i in range(7):
                try:
                    run_to_datetime = dt.datetime.strptime(times[i].text, dtoptions[i])
                    break
                except: pass
            run_to_ISO = re.split('T',dt.datetime.isoformat(run_to_datetime))[1]
            cat_dict['runs'].append({'run_uuid': str(uuid.uuid4()), 'time': run_to_ISO, 'name': names[i].text, 'vod': vod_link})
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
        except:
            try:
                next_category = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab active"]/following-sibling::a')
            except:
                try:
                    misc_button = self.driver.find_element(by=By.XPATH, value='//a[@id="miscellaneous"]')
                    misc_button.click()
                    next_category = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//a[@class="dropdown-item category active"]/following-sibling::a')))
                except:
                    next_category = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab"]')
                    done = True
        self.driver.execute_script(next_category.get_attribute('onclick'))
        time.sleep(0.5)
        print(f'[INFO] redirected to {self.driver.current_url}')
        return done # Use this to break a loop cycling through all categories


    def get_all_game_PBs(self) -> dict:
        '''
        Gets PBs for all categories for game with links and IDs for each category, stores this info in a dictionary.

        Returns:
            dict: a dictionary with info for all PBs for selected game
        '''
        game_dict = {'game_id': re.split('#',self.driver.current_url[25:])[0], 'game_uuid': str(uuid.uuid4()), 'category': []}
        done = False
        while done == False:
            done = self.next_cat()
            cat_dict = self.get_all_cat_PBs()
            game_dict['category'].append({'cat_id': self.driver.current_url[25:], 'cat_uuid': str(uuid.uuid4()), 'link': self.driver.current_url, 'runs': cat_dict})
        return game_dict

    def get_game_links(self, pages: int = 1) -> list:
        self.driver.get('https://www.speedrun.com/games')
        link_list = []
        games = self.driver.find_elements(by=By.XPATH, value='//*[@id="list"]//a')
        if pages != 1:
            for i in range(pages-1):
                games[len(games)-1].click()
                games = self.driver.find_elements(by=By.XPATH, value='//*[@id="list"]//a')
        for j in range(pages):
            for k in range(50):
                link_list.append(games[k+51*j].get_attribute('href'))
        return link_list
