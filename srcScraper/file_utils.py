import boto3
import json
import re
import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'srcboardscraper.co4inbd9d9j7.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = 'xzxzxzxzx'
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
engine.connect()

key = input('Access key ID: ')
skey = input('Secret key: ')
region = 'eu-west-2'
s3_client = boto3.client('s3',aws_access_key_id=key,aws_secret_access_key=skey,region_name=region)
s3 = boto3.resource('s3')
bucket = 'srdotcom-board-data'
my_bucket = s3.Bucket(bucket)
os.makedirs(os.getcwd()+'/srcScraper/board_data', exist_ok=True)

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

def check_game_already_scraped(URL: str, existing_data: list) -> bool:
    '''
    Checks if the current game has already been scraped.

    Args:
        str: current URL
    Returns:
        bool: True if game is found in s3 bucket, False if not found 
    '''
    count = existing_data.count(re.split('#',URL[25:])[0])
    if count > 0:
        print('[INFO] data for game already found')
        return True
    else: return False

def check_list_already_scraped(link_list: list, existing_data: list) -> list:
    '''
    Checks list found by scraper.get_game_links() to see which games are already scraped, returns list of unscraped games

    Args:
        list: list of links to games found by scraper.get_game_links()
        list: list of the IDs of all games in s3 bucket
    Returns:
        list: list of links to games in link_list that are not found in existing_data
    '''
    reduced_link_list = []
    for game in link_list:
        if game[25:] not in existing_data:
            reduced_link_list.append(game)
    return reduced_link_list

def save_and_upload_S3(game_dict: dict):
    '''
    Saves collected data as a .json file and uploads to s3 bucket.

    Args:
        dict: run data for current game (found by Scraper.get_all_game_PBs())
    '''
    file_name = game_dict['game_id']+'.json'
    file_path = os.getcwd()+'/srcScraper/board_data/'+file_name
    print(file_path)
    try:
        with open(file_path, mode='w') as f:
            json.dump(game_dict, f)
    except: print('1')
    try:
        s3_client.upload_file(file_path, bucket, file_name)
    except: print(2)
    

def upload_RDS(game_dict: dict):
    '''
    Uploads data for single game to RDS as SQL tables

    Args:
        dcit: run data for current game (found by Scraper.get_all_game_PBs())
    '''
    df = pd.DataFrame.from_dict(game_dict)
    df1 = pd.json_normalize(df['category'])
    for index,row in df1.iterrows():
        try:
            df2 = pd.json_normalize(row['runs'])
            df2.to_sql(row['cat_id'], engine, if_exists='replace')
            # print('[INFO] successfully uploaded '+row['cat_id']+' to RDS')
        except:
            # print('[ERROR] failed to upload '+row['cat_id']+' to RDS')
            pass

def upload_all_tables_from_bucket():
    '''
    Uploads data from S3 bucket to RDS as SQL tables
    '''
    for file in my_bucket.objects.all():
        key = file.key
        body = file.get()['Body'].read()
        try:
            df = pd.read_json(str(body)[2:len(str(body))-1])
            df1 = pd.json_normalize(df['category'])
            for index, row in df1.iterrows():
                try:
                    df2 = pd.json_normalize(row['runs'])
                    df2.to_sql(row['cat_id'], engine, if_exists='replace')
                    # print('[INFO] successfully uploaded '+row['cat_id']+' to RDS')
                except: pass
                    # print('[ERROR] failed to upload '+row['cat_id']+' to RDS')
        except: pass
            # print('[ERROR] failed to upload ' + key + ' to RDS')
