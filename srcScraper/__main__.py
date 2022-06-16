from scraper import Scraper
import file_utils
import json
import time
import os

# existing_data = file_utils.get_existing_data()
myScraper = Scraper()
link_list = myScraper.get_game_links(3)
# link_list = myScraper.get_all_game_links()
# reduced_link_list = file_utils.check_list_already_scraped(link_list, existing_data)

print('[INFO] games to be scraped:')
print(link_list)
# print(reduced_link_list)
# print('test0')
for game in link_list:
# for game in reduced_link_list:
    # print('test1')
    if game != None:
        # print('test2')
        myScraper.driver.get(game)
        print(f'[INFO] redirected to {myScraper.driver.current_url}')
        try:
            my_dict = myScraper.get_all_game_PBs()
        except: print('[ERROR] exception in get_all_game_PBs method')
        try:
            file_utils.save_and_upload_S3(my_dict)
        except: print('[ERROR] exception in save_and_upload_S3 method')
        try:
            file_utils.upload_RDS(my_dict)
        except: print('[ERROR] exception in upload_RDS method') 

last = ''
while True:
    time.sleep(60)
    last = myScraper.get_most_recent_run(last)
    try:
        my_dict = myScraper.get_all_game_PBs()
        file_utils.save_and_upload_S3(my_dict)
        file_utils.upload_RDS(my_dict)
    except: 
        print('[ERROR] exception in get_all_game_PBs method')
        pass