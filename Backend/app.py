from dotenv import load_dotenv
import os
import requests
import fastapi

load_dotenv()

API_KEY = os.getenv('my_API')
base_url = 'https://www.googleapis.com'

def get_analytics(channels):
    url = f'https://www.googleapis.com/youtube/v3/channels'

    params = {
    "key": API_KEY,
    "part": "snippet,statistics,contentDetails",
    "id": channels
    }
    
    response = requests.get(url, params=params)
    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        channel_data = response.json()

        if "items" in channel_data and len(channel_data["items"]) > 0:

            result = []

            for item in channel_data["items"]:
                analytic_dict = {}
                analytic_dict['channel_id'] = item.get("id")
                analytic_dict['video_title'] = item.get("snippet").get('title')
                analytic_dict['video_published_date'] = item.get("snippet").get('publishedAt')
                analytic_dict['video_url'] = item.get("snippet").get('customUrl')
                analytic_dict['video_likes'] = item.get("contentDetails").get('relatedPlaylists').get('likes')
                analytic_dict['subscribers'] = item.get("statistics").get('subscriberCount')

                result.append(analytic_dict)
           
    else:
        print('There was some problem')
        print(response.text)


channel_id = 'UCK8sQmJBp8GCxrOtXWBpyEA'
get_analytics(channel_id)