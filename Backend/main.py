from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analysis import get_channel_overview
from analysis import get_top_10_views
from analysis import get_top_10_engagement
from analysis import get_worst_10_engagement
from analysis import get_video_performance
from analysis import best_time_to_post
from analysis import best_time_to_post
from analysis import key_insight_summary
from analysis import correlation_view
from analysis import get_data 


#create fastapi app
app = FastAPI()

origins = [
    'http://localhost:5173'
]

app.add_middleware (
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

df = get_data()

@app.get('/')
def root():
    return {"message": "Welcome to the Video Analytics API"}

@app.get('/overview')
def overview():
    return get_channel_overview(df)

@app.get('/top_10_by_views')
def top_10_by_views():
    return get_top_10_views(df)

@app.get('/top_10_by_engagement')
def top_10_by_engagement():
    return get_top_10_engagement(df)

@app.get('/worst_10_by_engagement')
def worst_10_by_engagement():
    return get_worst_10_engagement(df)

@app.get('/video_performance')
def video_performance():
    return get_video_performance(df)

@app.get('/best_time_to_post')
def best_time_to_post_endpoint():
    return best_time_to_post(df)

@app.get('/key_insights')
def key_insights():
    return key_insight_summary(df)

@app.get('/correlation')
def correlation():
    return correlation_view(df)