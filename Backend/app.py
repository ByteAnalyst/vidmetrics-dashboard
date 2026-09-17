from dotenv import load_dotenv
import os
import requests
import fastapi

load_dotenv()

API_KEY = os.getenv('my_API')

def get_analytics(identifier):
    url = 'https://www.googleapis.com/youtube/v3/'

params = {
    "key": API_KEY,
    "part": "snippet,statistics,contentDetails"
}

response = requests.get()
data = response.json()
    