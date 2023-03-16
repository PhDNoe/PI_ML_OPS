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



import pandas as pd


def get_max_duration_inner(df:pd.DataFrame, year=None, platform=None, duration_type=None ):

    """
        Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.
    """
    
    df_filtered = df[['id','title','release_year','duration_int', 'duration_type']]
    if year!=None or  duration_type!=None or  platform!=None:
    
        if year!=None:
            cond_year = df_filtered['release_year']==year
        if platform!=None:
            cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
        if duration_type!=None:
            cond_dur_type = df_filtered['duration_type']==duration_type


        # Estan todas las condiciones
        if year!=None and  duration_type!=None and  platform!=None:
            mask = cond_year & cond_dur_type & cond_platform
        # Se cumplen dos condiciones
        elif  year!=None and  duration_type!=None:
            mask = cond_year & cond_dur_type        
        elif  year!=None and  platform!=None:
            mask = cond_year & cond_platform
        elif  duration_type!=None and  platform!=None:
            mask = cond_dur_type & cond_platform

        # Se cumple solo una condicion
        elif year!=None:
            mask = cond_year
        elif duration_type!=None:
            mask = cond_dur_type
        elif platform!=None:
            mask = cond_platform
    
    if not(year==None and  duration_type==None and  platform==None):
        # Aplico todos los filtros
        df_filtered = df_filtered[mask]

    # ordeno, y me quedo con el mas grande
    result = None
    if df_filtered.shape[0]>0:
        result = df_filtered.sort_values(by='duration_int',ascending=False).head(1).title.values[0]   
    return result



def get_score_count_inner(df:pd.DataFrame, platform, scored, year):
    """
        Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
    """

    df_filtered = df[['id','release_year', 'score']]

    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
    cond_year = df_filtered['release_year']==year
    cond_score = df_filtered['score']>scored
    mask = cond_platform & cond_year & cond_score    
    amount = df_filtered[mask].shape[0]
    # print("Amount --> ", amount)

    return amount

def get_count_platform_inner(df:pd.DataFrame, platform):
    """
        Cantidad de películas por plataforma con filtro de PLATAFORMA
    """
    df_filtered = df[['id']]
    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
    amount = df_filtered[cond_platform].shape[0]
    print(amount)
    return amount


def get_actor_inner(df:pd.DataFrame, platform, year):
    """ 
        Actor que más se repite según plataforma y año. 
    """

    df_filtered = df[['id',"release_year", "cast"]]

    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
    cond_year = df_filtered['release_year']==year
    mask = cond_platform & cond_year
    df_filtered = df_filtered[mask]

    df_filtered = df_filtered.query('cast != "unknown cast"')

    # separamos cada actor en su propia fila
    df_cast = df_filtered['cast'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('cast')

    # Contar la cantidad de ocurrencias de cada actor
    count_cast = df_cast['cast'].value_counts()
    
    # Seleccionar el actor con la mayor cantidad de ocurrencias
    most_common_cast = count_cast.idxmax()

    

    return most_common_cast