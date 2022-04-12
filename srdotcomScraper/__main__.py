from scraper import Scraper
import json

myScraper = Scraper()
myScraper.search('Spyro the dragon')
my_dict = myScraper.get_all_game_PBs()

with open('/home/guhch/AiCore/Data_Collection_Pipeline/data-collection-pipeline/srdotcomScraper/board_data/'+my_dict['game_id']+'.json', mode='w') as f:
    json.dump(my_dict, f)

myScraper.driver.quit()
