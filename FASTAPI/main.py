
# *****************************************************************************
#                              IMPORT ZONE
# *****************************************************************************
from fastapi import FastAPI
from my_functions import *
import pandas as pd
import asyncio
from enum import Enum
from data_types import PlatformOptions, DurationOptions


# *****************************************************************************
#                        API INIT AND ASYNC FETCH DATA
# *****************************************************************************

# Load the data asynchronously and return the DataFrame
async def load_data():
    df1 = pd.read_csv('./data/all_together_with_score.csv')
    df1.drop(columns=['Unnamed: 0'], inplace=True)
    return df1


app = FastAPI()


# Save asynchronously fetched data to a global variable
@app.on_event("startup")
async def startup():
    global df
    df = await load_data()



# *****************************************************************************
#                           ROUTE ZONE
# *****************************************************************************

@app.get("/api")
async def get_root():
    return {"routes":{
        "/api/max_duration": "Movie with longer duration with optional filters of year, platform and duration_type",
        "/api/score_count": "Number of films by platform with a score greater than XX in a given year",
        "/api/count_platform": "Number of movies per platform. The platform must be specified.",
        "/api/actor": "Actor who appears the most times according to platform and year. "
    }}


@app.get("/api/max_duration")
async def get_max_duration(year: int = None, platform: PlatformOptions = None, duration_type: DurationOptions = None):
    """
        This async function returns the movie with longer duration with optional filters of year, 
        platform and duration_type

        Invocation example:
        http://localhost:8000/api/max_duration?year=2020&platform=Netflix&duration_type=min

        All 3 query params (year, platform and duration_type) are optional
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Wait until the DataFrame is available before calling the function
    while df.empty:
        await asyncio.sleep(1)

    # Inner function invocation
    movie = get_max_duration_inner(df, year=year, platform=platform, duration_type=duration_type)
    
    
    if movie is None:
        return {"message": "No results"}
    return {"movie": movie}



@app.get("/api/score_count")
async def get_score_count(platform: PlatformOptions, scored: float, year: int):
    """
        This async function returns the number of films by platform with a score 
        greater than XX in a given year


        Invocation example:
        http://localhost:8000/api/score_count?platform=Netflix&scored=3.5&year=2020
        
        All 3 query params are required
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Wait until the DataFrame is available before calling the function
    while df.empty:
        await asyncio.sleep(1)
    
    # Inner function
    amount = get_score_count_inner(df, platform, scored, year)
    return {"number_of_films": amount}



@app.get("/api/count_platform")
async def get_count_platform(platform: PlatformOptions):
    """
        This async function returns the number of movies per platform. 

        Invocation example:
        http://localhost:8000/api/count_platform?platform=Netflix

        platform parameter is required
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Wait until the DataFrame is available before calling the function
    while df.empty:
        await asyncio.sleep(1)

    # Inner function
    amount = get_count_platform_inner(df, platform)
    return {"number_of_films": amount}



@app.get("/api/actor")
async def get_actor(platform: PlatformOptions, year: int):
    """
        This async function returns the actor who appears the most times according to platform and year
        
        Invocation example:
        http://localhost:8000/api/actor?platform=Netflix&year=2019

        Both parameters (platform and year) are required.
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Wait until the DataFrame is available before calling the function
    while df.empty:
        await asyncio.sleep(1)

    # Inner function
    actor = get_actor_inner(df, platform, year)
    if actor!=None:
        return {"actor": actor}
    else:
        return {"message": "No results"}