from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time

class scraper:
    def __init__(self,URL):
        self.URL = URL
        self.driver = webdriver.Firefox()

    # Loads site and accepts cookies (on sr.com)
    def load_site(self) -> webdriver.Firefox:
        self.driver.get(self.URL)
        delay = 10
        try:
            accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="fc-button fc-cta-consent fc-primary-button"]')))
            accept_cookies_button.click()
            print('[INFO] cookies accepted')
            time.sleep(1)
        except TimeoutException:
            print('[ERROR] timeout exception when trying to accept cookies')

    # Searches for 'query' in the search bar and chooses the first result
    '''
    TO DO: -FIGURE OUT HOW TO SEARCH ONLY THE GAMES LIST, IGNORING THE SERIES LIST
           -MAYBE IMPLEMENT searchGame AND searchUser AS SEPARATE FUNCTIONS
    '''
    def search(self,query):
        search_bar = self.driver.find_element(by=By.XPATH, value='//*[@type="search"]')
        search_bar.click()
        time.sleep(0.5)
        search_bar.send_keys(query)
        time.sleep(0.5)
        try:
            result = self.driver.find_element(by=By.XPATH, value='//*[@class="ui-menu-item"]')
            result.click()
            print(f'[INFO] redirected to {self.driver.current_url}')
            time.sleep(0.5)
        except:
            print('[ERROR] no results found')
        

    # Collects all the times on the leaderboard for selected category (i.e. PBs of all players with runs on the board) + name of runner + link to VOD
    def getAllCatPBs(self):
        pass

    # Switches page to next category. If on last category, returns to the initial category
    def nextCat(self):
        done = False
        try:
            misc_button = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab active"]/following-sibling::a[1][@id="miscellaneous"]')
            misc_button.click()
            next_cat = self.driver.find_element(by=By.XPATH, value='//a[@class="dropdown-item category"]')
            print('1')
        except:
            try:
                next_cat = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab active"]/following-sibling::a')
                print('2')
            except:
                try:
                    misc_button = self.driver.find_element(by=By.XPATH, value='//a[@id="miscellaneous"]')
                    misc_button.click()
                    next_cat = self.driver.find_element(by=By.XPATH, value='//a[@class="dropdown-item category active"]/following-sibling::a')
                    print('3')
                except:
                    next_cat = self.driver.find_element(by=By.XPATH, value='//a[@class="category category-tab"]')
                    done = True
                    print('4')
        next_cat.click()
        time.sleep(0.5)
        return done # Use this to break a loop cycling through all categories

    # Gets links to all categories
    def getCatLinks(self):
        link_list = []
        done = False
        while done == False: # go next cat then store link so that specific link for initial cat is stored
            done = self.nextCat()
            link_list.append(self.driver.current_url)
        return link_list
            


if __name__ == "__main__":
    myScraper = scraper('https://www.speedrun.com')
    myScraper.load_site()
    myScraper.search('Spyro the dragon')
    cat_links = myScraper.getCatLinks()
    print(cat_links)
    myScraper.driver.quit()
