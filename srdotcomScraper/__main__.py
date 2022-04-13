from scraper import Scraper
import file_utils
import json

myScraper = Scraper()
link_list = myScraper.get_game_links()
print(link_list)
# myScraper.search('minecraft')
for game in link_list:
    myScraper.driver.get(game)
    if not file_utils.check_already_scraped(myScraper.driver.current_url):
        my_dict = myScraper.get_all_game_PBs()
        file_utils.save_and_upload(my_dict)

myScraper.driver.quit()
