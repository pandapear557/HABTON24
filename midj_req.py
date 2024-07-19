import json
import requests
import csv

with open("./config.json", "r") as json_file:
    params = json.load(json_file)

import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('midj.csv')
all_text = ' '.join(df.astype(str).values.flatten())

header = {
    'authorization': params['authorization']
}

prompt = all_text
payload = {
    'type': 2, 
    'application_id': params['application_id'],
    'guild_id': params['guild_id'],
    'channel_id': params['channelid'],
    'session_id': params['session_id'],
    'data': {
        'version': params['version'],
        'id': params['id'],
        'name': 'imagine',
        'type': 1,
        'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + params['flags']}],
        'attachments': []
    }
}

r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)

print(f'prompt {prompt} successfully sent!')