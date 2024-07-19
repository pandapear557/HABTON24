import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
import requests
import os

# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = './src/client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/photoslibrary'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials
def get_access_token():
    credentials = authorize_credentials()
    access_token = credentials.access_token
    return access_token

def getPhotoUrl(access_token, photo_id):
    # Set the headers for the request
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-type": "application/json"
    }

    # Set the URL for the request
    url = "https://photoslibrary.googleapis.com/v1/mediaItems/" + photo_id

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Parse the response as JSON
    response_json = response.json()

    # Get the URL of the photo from the response
    photo_url = response_json["baseUrl"]
    return photo_url

def uploadPhoto(img):
    access_token = get_access_token()
    # Set up the request headers
    headers = {
        'Authorization': 'Bearer %s' % access_token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Content-Type': 'image/jpeg',
        'X-Goog-Upload-Protocol': 'raw'
    }

    image_path = img
    # Read the binary data from file
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Send the POST request to get the upload token
    response = requests.post('https://photoslibrary.googleapis.com/v1/uploads',
                            headers=headers, data=image_data)

    # Check if the request was successful and get the upload token
    if response.status_code == requests.codes.ok:
        upload_token = response.text
        headers = {
            'Authorization': 'Bearer %s' % access_token,
            'Content-type': 'application/json'
        }
        payload = {
            "newMediaItems": [
                    {
                        "simpleMediaItem": {
                            "fileName": os.path.basename(image_path),
                            "uploadToken": upload_token
                        }
                    }
                ]
            }
        # Send the POST request to get the upload token
        response = requests.post('https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate',
                                headers=headers, json=payload)   
        json_response = response.json()
        photo_id = json_response['newMediaItemResults'][0]['mediaItem']['id']
        #If you want to get public url for anyone can see 
        photo_url = getPhotoUrl(access_token, photo_id)
        print("mediaItems full response = ",json_response,'\n\n\n',"public url = ", photo_url)
    else:
        response.raise_for_status()

if __name__ == "__main__":
    uploadPhoto("./src/test_photo")

