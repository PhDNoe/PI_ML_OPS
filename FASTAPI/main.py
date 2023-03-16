
# ***********************************************************************************************************************
#    ESPECIFICACIONES DE LA API

#  1) Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
#  (la función debe llamarse get_max_duration(year, platform, duration_type))

#  2) Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
#  (la función debe llamarse get_score_count(platform, scored, year))

#  3) Cantidad de películas por plataforma con filtro de PLATAFORMA. 
#  (La función debe llamarse get_count_platform(platform))

#  4) Actor que más se repite según plataforma y año. 
# (La función debe llamarse get_actor(platform, year))

from fastapi import FastAPI
from my_functions import *
import pandas as pd
import asyncio



# Carga los datos y retorna el DataFrame
async def load_data():
    df1 = pd.read_csv('./data/all_together_with_score.csv')
    df1.drop(columns=['Unnamed: 0'], inplace=True)
    return df1


app = FastAPI()


# Carga los datos de manera asíncrona y crea una variable global para el DataFrame
@app.on_event("startup")
async def startup():
    global df
    df = await load_data()

@app.get("/")
async def get_root():
    return {"rutas":{
        "/api/max_duration": "Movie with longer duration with optional filters of year, platform and duration_type",
        "/api/score_count": "Number of films by platform with a score greater than XX in a given year",
        "/api/count_platform": "Number of movies per platform. The platform must be specified.",
        "/api/actor": "Actor who appears the most times according to platform and year. "
    }}


@app.get("/api/max_duration")
async def get_max_duration(year: int = None, platform: str = None, duration_type: str = None):
    """
        Ejemplo de invocacion:
        http://localhost:8000/api/max_duration?year=2020&platform=Netflix&duration_type=min
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Espera hasta que el DataFrame esté disponible antes de llamar a la función
    while df.empty:
        await asyncio.sleep(1)


    movie = get_max_duration_inner(df, year=year, platform=platform, duration_type=duration_type)
    return {"message": movie}



@app.get("/api/score_count")
async def get_score_count(platform: str, scored: float, year: int):
    """
        Ejemplo de invocacion:
        http://localhost:8000/api/score_count?platform=Netflix&scored=3.5&year=2020
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Espera hasta que el DataFrame esté disponible antes de llamar a la función
    while df.empty:
        await asyncio.sleep(1)
    
    amount = get_score_count_inner(df, platform, scored, year)
    return {"message": amount}



@app.get("/api/count_platform")
async def get_count_platform(platform: str):
    """
        Ejemplo de invocacion:
        http://localhost:8000/api/count_platform?platform=Netflix
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Espera hasta que el DataFrame esté disponible antes de llamar a la función
    while df.empty:
        await asyncio.sleep(1)

    amount = get_count_platform_inner(df, platform)
    return {"message": amount}



@app.get("/api/actor")
async def get_actor(platform: str, year: int):
    """
        Ejemplo de invocacion:
        http://localhost:8000/api/actor?platform=Netflix&year=2019
    """
    global df
    if df.empty:
        return {"message": "DataFrame not loaded yet"}
    
    # Espera hasta que el DataFrame esté disponible antes de llamar a la función
    while df.empty:
        await asyncio.sleep(1)


    actor = get_actor_inner(df, platform, year)
    return {"message": actor}