import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app import get_analytics
from app import get_video_id
from app import get_videos

channel_results = get_analytics(channels=['UC_x5XG1OV2P6uZZ5FSM9Ttw'])  
uploads_id =  channel_results[0].get('uploads')
video_ids = get_video_id(uploads_id)
video_rows = get_videos(video_ids)

df = pd.DataFrame(video_rows)

# Data Cleaning
df = df.dropna(subset=['video_id', 'published_date', 'channel_id'])
df = df.drop_duplicates(subset=['video_id'])
df = df[['video_id', 'published_date', 'channel_id', 'title', 'view_count', 'like_count', 'comment_count']]
df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')

# EDA

