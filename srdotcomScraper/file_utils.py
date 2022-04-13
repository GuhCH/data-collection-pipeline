import boto3
import json
import re

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = 'srdotcom-board-data'
my_bucket = s3.Bucket(bucket)

def get_existing_data() -> list:
    '''
    Gets a list of readable IDs for games which have been scraped (i.e. have data saved in the s3 bucket).

    Returns:
        list: a list of the IDs of all games in s3 bucket 
    '''
    existing_games = []
    for file in my_bucket.objects.all():
        existing_games.append(file.key[:len(file.key)-5])
    return existing_games

def check_already_scraped(URL: str) -> bool:
    '''
    Checks if the current game has already been scraped.

    Args:
        str: current URL
    Returns:
        bool: True if game is found in s3 bucket, False if not found 
    '''
    existing_data = get_existing_data()
    count = existing_data.count(re.split('#',URL[25:])[0])
    if count > 0:
        print('[INFO] data for game already found')
        return True
    else: return False

def save_and_upload(game_dict: dict):
    '''
    Saves collected data as a .json file and uploads to s3 bucket.

    Args:
        dict: run data for current game (found by Scraper.get_all_game_PBs())
    '''
    file_name = game_dict['game_id']+'.json'
    file_path = '/home/guhch/AiCore/Data_Collection_Pipeline/data-collection-pipeline/srdotcomScraper/board_data/'+file_name
    with open(file_path, mode='w') as f:
        json.dump(game_dict, f)
    s3_client.upload_file(file_path, bucket, file_name)
