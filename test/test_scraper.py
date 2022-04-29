import unittest
from scraper import Scraper

class scraperTestCase(unittest.TestCase):

    def setUp(self):
        self.myScraper = Scraper('https://www.speedrun.com')


    def test_load_site(self):
        expected_URL = 'https://www.speedrun.com/'
        self.assertEqual(expected_URL, self.myScraper.driver.current_url)
        self.myScraper.driver.quit()


    def test_search_0(self):
        self.myScraper.search('minecraft: java edition')
        expected_URL = 'https://www.speedrun.com/mc'
        self.assertEqual(expected_URL, self.myScraper.driver.current_url)

    def test_search_1(self):
        self.myScraper.search('jak and daxter: the')
        expected_URL = 'https://www.speedrun.com/jak1'
        self.assertEqual(expected_URL, self.myScraper.driver.current_url)

    def test_search_2(self):
        self.myScraper.search('spyro the dragon')
        expected_URL = 'https://www.speedrun.com/spyro1'
        self.assertEqual(expected_URL, self.myScraper.driver.current_url)


    def test_get_all_cat_PBs(self):
        self.myScraper.driver.get('https://www.speedrun.com/spyro1#120')
        expected_100th_run = {'time': '1h 44m 59s','name': 'stuser', 'vod': 'https://www.speedrun.com/spyro1/run/ylr159xy'}
        cat_dict = self.myScraper.get_all_cat_PBs()
        self.assertEqual(expected_100th_run, cat_dict['runs'][99])
        print('[INFO] if this test fails, go check the spyro 1 120 board as the expected result may have changed')


    def test_next_cat(self):
        done = False
        i = 0
        self.myScraper.driver.get('https://www.speedrun.com/spyro1')
        test_URLs = ['https://www.speedrun.com/spyro1#120','https://www.speedrun.com/spyro1#Cheat','https://www.speedrun.com/spyro1#80_Dragons','https://www.speedrun.com/spyro1#Vortex','https://www.speedrun.com/spyro1#Any']
        while done == False:
            done = self.myScraper.next_cat()
            self.assertEqual(test_URLs[i], self.myScraper.driver.current_url)
            i += 1
        self.assertEqual(i, 5)


    def test_get_all_game_PBs(self):
        self.myScraper.driver.get('https://www.speedrun.com/spyro1')
        myDict = self.myScraper.get_all_game_PBs()
        ids = []
        expected_ids = ['spyro1#120','spyro1#Cheat','spyro1#80_Dragons','spyro1#Vortex','spyro1#Any']
        for i in range(5):
            ids.append(myDict['category'][i]['id'])
        self.assertEqual(ids, expected_ids)
        

    def tearDown(self):
        self.myScraper.driver.quit()
        del self.myScraper

unittest.main(argv=[''], verbosity=2, exit=False)