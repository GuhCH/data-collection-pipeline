import boto3
import json

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = 'srdotcom-board-data'
my_bucket = s3.Bucket(bucket)

def get_existing_data() -> list:
    existing_games = []
    for file in my_bucket.objects.all():
        existing_games.append(file.key[:len(file.key)-5])
    return existing_games

def check_already_scraped(URL: str) -> bool:
    existing_data = get_existing_data()
    count = existing_data.count(URL[25:])
    if count > 0:
        print('[INFO] data for game already found')
        return True
    else: return False

def save_and_upload(game_dict: dict):
    file_name = game_dict['game_id']+'.json'
    file_path = '/home/guhch/AiCore/Data_Collection_Pipeline/data-collection-pipeline/srdotcomScraper/board_data/'+file_name
    with open(file_path, mode='w') as f:
        json.dump(game_dict, f)
    s3_client.upload_file(file_path, bucket, file_name)

if __name__ == '__main__':
    
    is_scraped = check_already_scraped('https://www.speedrun.com/mc')
    print(is_scraped)