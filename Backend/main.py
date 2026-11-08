from fastapi import FastAPI
from analysis import get_channel_overview
from analysis import get_top_10_views
from analysis import get_top_10_engagement
from analysis import get_worst_10_engagement
from analysis import get_monthly_performance
from analysis import dataframe 

df = dataframe()
#create fastapi app
app = FastAPI()
@app.get('/')
def root():
    return {"message": "Welcome to the Video Analytics API"}

@app.get('/overview/{channel_id}')
def overview(channel_id: str):
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

@app.get('/monthly_performance')
def monthly_performance():
    return get_monthly_performance(df)

