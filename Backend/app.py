from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv('my_API')
channel_url = 'https://www.googleapis.com/youtube/v3/channels'
playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
videos_url = 'https://www.googleapis.com/youtube/v3/videos'


#channel id
def get_analytics(channels):
    empty_channel_list = []
    params = {
    "key": API_KEY,
    "part": "snippet,statistics,contentDetails",
    "id": channels
    }
    
    response = requests.get(channel_url, params=params)
    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        channel_data = response.json()

        if "items" in channel_data and len(channel_data["items"]) > 0:

            result_channel = []

            for item in channel_data["items"]:
                channel_dict = {}
                channel_dict['channel_id'] = item.get("id")
                channel_dict['channel_title'] = item.get("snippet", {}).get('title')
                channel_dict['channel_published_date'] = item.get("snippet", {}).get('publishedAt')
                channel_dict['channel_url'] = item.get("snippet", {}).get('customUrl')
                channel_dict['uploads'] = item.get("contentDetails", {}).get('relatedPlaylists', {}).get('uploads')
                channel_dict['videoCount'] = item.get("statistics", {}).get('videoCount')
                channel_dict['subscribers'] = item.get("statistics", {}).get('subscriberCount')

                result_channel.append(channel_dict)
            return result_channel
           
    else:
        print('There was some problem')
        print(response.text)
        return []
    return []
channel_id = 'UCK8sQmJBp8GCxrOtXWBpyEA'



#video id

def get_video_id(uploads_id):
    empty_video_list = []
    params = {
    'key': API_KEY,
    'part': 'contentDetails',
    'playlistId': uploads_id,
    'maxResults': 50
    }

    response = requests.get(playlist_url, params=params)
    
    if response.status_code == 200:
        video_id_data = response.json()

        if 'items' in video_id_data and len(video_id_data['items']) > 0:
            result_ids = []

            for item in video_id_data["items"]:
                video_dict = {}
                video_dict['id'] = item.get("contentDetails", {}).get('videoId')
                result_ids.append(video_dict)
            return result_ids
           
    else:
        print('There was some problem')
        print(response.text)            
        return []
    return []
def get_videos(ids_list):
    empty_videos_list = []
    if ids_list and isinstance(ids_list[0], dict):
        video_ids = [item.get('id') for item in ids_list if item.get('id')]
    else:
        video_ids = [item for item in ids_list if item]

    if not video_ids:
        return []

    ids_string = ",".join(video_ids)

    params = {
        'key': API_KEY,
        'part': 'snippet,statistics',
        'id': ids_string
    }

    response = requests.get(videos_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            ids = []

            for item in data["items"]:
                video_row = {}
                video_row['video_id'] = item.get("id")
                video_row['published_date'] = item.get("snippet", {}).get('publishedAt')
                video_row['channel_id'] = item.get("snippet", {}).get('channelId')
                video_row['title'] = item.get("snippet", {}).get('title')
                video_row['view_count'] = int(item.get("statistics", {}).get('viewCount', 0))
                video_row['like_count'] = int(item.get("statistics", {}).get('likeCount', 0))
                video_row['comment_count'] = int(item.get("statistics", {}).get('commentCount', 0))
                ids.append(video_row)
            return ids
    else:
        print('There was some problem')
        print(response.text)
        return []
    return []
channel_results = get_analytics(channel_id)
if channel_results:
    uploads_id =  channel_results[0].get('uploads')
    video_ids = get_video_id(uploads_id)
    video_rows = get_videos(video_ids)
else:
    print("No Results were found")
