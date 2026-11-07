import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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

#Channel Overview Cards
#total views
if 'view_count' in df.columns and not df['view_count'].isnull().all():
    total_views = df['view_count'].sum()
    print(f'Total Views: {total_views}')
else:
    print('No views')

#total likes
if 'like_count' in df.columns and not df['like_count'].isnull().all():
    total_likes = df['like_count'].sum()
    print(f'Total Likes: {total_likes}')
else:
    print('No Likes')

#total comments
if 'comment_count' in df.columns and not df['comment_count'].isnull().all():
    total_comments = df['comment_count'].sum()
    print(f'Total Comments: {total_comments}')
else:
    print('No Comments')

#average views per video

if 'view_count' in df.columns and not df['view_count'].isnull().all():
    average_views = int(df['view_count'].mean())
    print(f'Average Views: {average_views}')
else:
    print('No views')


# average engagment
if 'view_count' in df.columns and 'like_count' in df.columns and 'comment_count' in df.columns and not df['view_count'].isnull().all() and not df['like_count'].isnull().all() and not df['comment_count'].isnull().all():
    engagement = df['view_count'] + df['like_count'] + df['comment_count']
    average_engagement = int(engagement.mean())
    print(f'Average Engagement: {average_engagement}')
else:
    print('No Engagement')


#engagement rate column
if 'view_count' in df.columns and 'like_count' in df.columns and 'comment_count' in df.columns and not df['view_count'].isnull().all() and not df['like_count'].isnull().all() and not df['comment_count'].isnull().all():
    df['engagement_rate'] = (df['like_count'] + df['comment_count']) / df['view_count']
