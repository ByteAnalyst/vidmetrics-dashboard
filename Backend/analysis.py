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
    return pd.DataFrame()

df = get_data()

# Data Cleaning
if not df.empty:
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
            "average_engagement": 0.0
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
PERIODS = {'day': 'D', 'week': 'W', 'month': 'M', 'year': 'Y'}

def get_video_performance(df, period='month'):
    if 'published_date' not in df.columns or df['published_date'].isnull().all():
        return []

    freq = PERIODS.get(period, 'M')
    dates = pd.to_datetime(df['published_date'], errors='coerce').dt.tz_localize(None)

    video_performance = (
        df.groupby(dates.dt.to_period(freq))
        .agg({
            'view_count': 'sum',
            'like_count': 'sum',
            'comment_count': 'sum',
            'video_id': 'count'
        })
        .reset_index()
        .sort_values(by='published_date', ascending=True)
    )

    video_performance['engagement_rate'] = (
        (video_performance['like_count'] + video_performance['comment_count'])
        / video_performance['view_count']
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    video_performance['published_date'] = video_performance['published_date'].astype(str)
    return video_performance.to_dict(orient='records')

def best_time_to_post(df):
    if 'published_date' in df.columns and not df['published_date'].isnull().all():
        df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
        df['hour'] = df['published_date'].dt.hour
        best_time = df.groupby('hour').agg({
            'view_count': 'sum',
            'like_count': 'sum',
            'comment_count': 'sum',
            'video_id': 'count'}).reset_index()
        best_time = best_time.sort_values(by='view_count', ascending=False)
        return best_time.to_dict(orient='records')

def correlation_view(df):
    if 'view_count' in df.columns and 'like_count' in df.columns and 'comment_count' in df.columns and not df['view_count'].isnull().all() and not df['like_count'].isnull().all() and not df['comment_count'].isnull().all():
        correlation = df[['view_count', 'like_count', 'comment_count']].corr()
        return correlation.to_dict()
    return {}

def key_insight_summary(df):
    # most viewed video
    if 'view_count' in df.columns and not df['view_count'].isnull().all():
        most_viewed_video = df.loc[df['view_count'].idxmax()]
        most_viewed_video_title = most_viewed_video['title']
        most_viewed_video_views = most_viewed_video['view_count']
        most_viewed_video_insight = f"The most viewed video is '{most_viewed_video_title}' with {most_viewed_video_views} views."
    else:
        most_viewed_video_insight = "No data available for most viewed video."

    # most liked video
    if 'like_count' in df.columns and not df['like_count'].isnull().all():
        most_liked_video = df.loc[df['like_count'].idxmax()]
        most_liked_video_title = most_liked_video['title']
        most_liked_video_likes = most_liked_video['like_count']
        most_liked_video_insight = f"The most liked video is '{most_liked_video_title}' with {most_liked_video_likes} likes."
    else:
        most_liked_video_insight = "No data available for most liked video."

    # best time to post
    best_time = best_time_to_post(df)
    if not best_time:
        best_time_insight = "No data available for best posting time."
    else:
        best_hour = best_time[0]['hour']
        best_time_insight = f"The best time to post is {best_hour}:00."

    return [most_viewed_video_insight, most_liked_video_insight, best_time_insight]