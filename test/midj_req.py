import json
import requests

with open("../src/config.json", "r") as json_file:
    params = json.load(json_file)

header = {
    'authorization': params['authorization']
}

prompt = "Rainy day paintings of Manet and Van Gogh. --v 5.0"

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