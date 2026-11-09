import pandas as pd
import numpy as np
from app import get_analytics
from app import get_video_id
from app import get_videos

channel_results = get_analytics(channels=['UC_x5XG1OV2P6uZZ5FSM9Ttw'])  
uploads_id =  channel_results[0].get('uploads')
video_ids = get_video_id(uploads_id)
video_rows = get_videos(video_ids)

#dataframe creation
def get_data():
    #engagement rate column
    df = pd.DataFrame(video_rows)
    if 'view_count' in df.columns and 'like_count' in df.columns and 'comment_count' in df.columns and not df['view_count'].isnull().all() and not df['like_count'].isnull().all() and not df['comment_count'].isnull().all():
        df['engagement_rate'] = (df['like_count'] + df['comment_count']) / df['view_count']
        return pd.DataFrame(df)
    return []

df = get_data()

# Data Cleaning
df = df.dropna(subset=['video_id', 'published_date', 'channel_id'])
df = df.drop_duplicates(subset=['video_id'])
df = df[['video_id', 'published_date', 'channel_id', 'title', 'view_count', 'like_count', 'comment_count', 'engagement_rate']]
df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')

# EDA

#Channel Overview Cards
def get_channel_overview(df):

    total_views = int(df['view_count'].sum()) if 'view_count' in df.columns and not df['view_count'].isnull().all() else 0
    total_likes = int(df['like_count'].sum()) if 'like_count' in df.columns and not df['like_count'].isnull().all() else 0
    total_comments = int(df['comment_count'].sum()) if 'comment_count' in df.columns and not df['comment_count'].isnull().all() else 0
    average_views = df['view_count'].mean() if 'view_count' in df.columns and not df['view_count'].isnull().all() else 0
    if 'like_count' in df.columns and 'comment_count' in df.columns and not df['like_count'].isnull().all() and not df['comment_count'].isnull().all():
        engagement = df['like_count'] + df['comment_count']
        average_engagement = engagement.mean()
        return {
            "total_views": int(total_views),
            "total_likes": int(total_likes),
            "total_comments": int(total_comments),
            "average_views": float(average_views),
            "average_engagement": float(average_engagement)
        }

#top 10 videos by views
def get_top_10_views(df):
    if 'view_count' in df.columns and not df['view_count'].isnull().all():
        top_10_views = df.nlargest(10, 'view_count')[['title', 'view_count', 'published_date', 'engagement_rate']]
        if 'published_date' in top_10_views.columns:
            top_10_views['published_date'] = top_10_views['published_date'].astype(str)
        return top_10_views.to_dict(orient = 'records')
    return []

#top 10 videos by engagement rate
def get_top_10_engagement(df):
    if 'engagement_rate' in df.columns and not df['engagement_rate'].isnull().all():
        top_10_engagement = df.nlargest(10, 'engagement_rate')[['title', 'view_count', 'published_date', 'engagement_rate']]
        if 'published_date' in top_10_engagement.columns:
            top_10_engagement['published_date'] = top_10_engagement['published_date'].astype(str)
        return top_10_engagement.to_dict(orient = 'records')
    return []
    

#worst 10 videos by engagement rate and views
def get_worst_10_engagement(df):
    if 'engagement_rate' in df.columns and not df['engagement_rate'].isnull().all():
        worst_10_engagement = df.nsmallest(10, 'engagement_rate')[['title', 'view_count', 'published_date', 'engagement_rate']]
        if 'published_date' in worst_10_engagement.columns:
            worst_10_engagement['published_date'] = worst_10_engagement['published_date'].astype(str)
        return worst_10_engagement.to_dict(orient = 'records')
    return []

#performance over time
def get_monthly_performance(df):
    if 'published_date' in df.columns and not df['published_date'].isnull().all():
        df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
        monthly_performance = df.groupby(
            df['published_date'].dt.to_period('M')).agg({
                'view_count': 'sum',
                'like_count': 'sum',
                'comment_count': 'sum',
                'video_id': 'count'}).reset_index()
        return {
            "monthly_performance": monthly_performance.to_dict(orient='records')
        }