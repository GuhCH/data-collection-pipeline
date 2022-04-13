from scraper import Scraper
import file_utils
import json

myScraper = Scraper()
myScraper.search('minecraft')
if not file_utils.check_already_scraped(myScraper.driver.current_url):
    my_dict = myScraper.get_all_game_PBs()
    file_utils.save_and_upload(my_dict)

myScraper.driver.quit()
