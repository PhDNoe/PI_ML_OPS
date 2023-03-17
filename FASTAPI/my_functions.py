import pandas as pd


def get_max_duration_inner(df:pd.DataFrame, year=None, platform=None, duration_type=None ):

    """
        This function returns the movie with longer duration with optional filters of year, 
        platform and duration_type
    """
    
    df_filtered = df[['id','title','release_year','duration_int', 'duration_type']]
    

    cond_year =  df_filtered['release_year'] == year if year else pd.Series(True, index=df_filtered.index)
    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0]) if platform else pd.Series(True, index=df_filtered.index)
    cond_dur_type = df_filtered['duration_type']==duration_type.lower() if duration_type else pd.Series(True, index=df_filtered.index)
    mask = cond_year & cond_platform & cond_dur_type
    df_filtered = df_filtered[mask]
    
    
    # Sort and get biggest
    result = None
    if df_filtered.shape[0]>0:
        result = df_filtered.sort_values(by='duration_int',ascending=False).head(1).title.values[0]   
    return result



def get_score_count_inner(df:pd.DataFrame, platform, scored, year):
    """
        This function returns the number of films by platform with a score 
        greater than XX in a given year
    """

    df_filtered = df[['id','release_year', 'score']]

    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
    cond_year = df_filtered['release_year']==year
    cond_score = df_filtered['score']>scored
    mask = cond_platform & cond_year & cond_score    
    amount = df_filtered[mask].shape[0]
    

    return amount



def get_count_platform_inner(df:pd.DataFrame, platform):
    """
        This function returns the number of movies per platform. 
    """
    df_filtered = df[['id']]
    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
    amount = df_filtered[cond_platform].shape[0]
    
    return amount
import pandas as pd


def get_actor_inner(df:pd.DataFrame, platform, year):
    """ 
        This async function returns the actor who appears the most times according to platform and year
    """

    df_filtered = df[['id',"release_year", "cast"]]

    cond_platform = df_filtered['id'].str.startswith(platform.lower()[0])
    cond_year = df_filtered['release_year']==year
    mask = cond_platform & cond_year
    df_filtered = df_filtered[mask]

    most_common_cast = None
    if not df_filtered.empty :
        # discard "unknown cast"
        df_filtered = df_filtered.query('cast != "unknown cast"')

        # separate each actor in its own row
        df_cast = df_filtered['cast'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('cast')

        # Count the number of occurrences of each actor
        count_cast = df_cast['cast'].value_counts()
        
        # Select the actor with the most occurrences
        most_common_cast = count_cast.idxmax()

    

    return most_common_cast