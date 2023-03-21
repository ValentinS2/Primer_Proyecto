from fastapi import FastAPI
import pandas as pd
import numpy as np
from fastapi.responses import HTMLResponse

df= pd.read_csv('DF_consultas.csv' , sep=",")

app= FastAPI()
@app.get("/", response_class=HTMLResponse)
async def main():
    
    button_html = """
    <h2>Bienvenidos a mi primera API</h2>
    <form>
        <button formaction="/docs">Ir a las Funciones</button>
    
        <br>
        
        <button formaction="/prediccion">Recomendación de Películas</button>
        <br>
        <button formaction="/prediccion">Salir</button>
    </form>
    """
    return button_html


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/get_max_duration")
def get_max_duration(release_year: int = None, source: str = None, duration_type: str = None):
    # Cargar el archivo CSV en un DataFrame de Pandas
    global df

    # Filtrar el DataFrame
    if duration_type is not None:
        filtered_df = df[df['duration_type'] == duration_type]
    else:
        filtered_df = df.copy()
    if release_year is not None:
        filtered_df = filtered_df[filtered_df['release_year'] == release_year]
    if source is not None:
        filtered_df = filtered_df[filtered_df['source'] == source]

    # Ordenar el DataFrame y obtener la fila con la duración máxima
    sorted_df = filtered_df.sort_values(by='duration_int', ascending=False)
    max_duration = sorted_df.iloc[0][['title']]

    return max_duration

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



@app.get("/get_score_count/{plataforma}/{ScoreMedio}/{release_year}")
def get_score_count(plataforma: str, ScoreMedio: int, release_year:int):
    global df
    # Contar el número de veces que se cumple la condición
    cantidad = np.count_nonzero(np.where((df["plataforma"] == plataforma) & (df["ScoreMedio"] >=ScoreMedio) & (df["release_year"] == release_year), True, False))

    # Devolver la cantidad de veces que se cumple la condición
    return cantidad

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



@app.get("/get_count_platform/{source}")
def get_count_platform(source:str):
    # Cargar el archivo CSV en un DataFrame de Pandas
    global df

    # Filtrar por plataforma
    filtered_df = df[df['source'] == source]

    # Contar la cantidad de películas por plataforma
    result = filtered_df.groupby('source').size().reset_index(name='count')

    return result.to_dict(orient='records')


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



@app.get("/get_actor({source}/{release_year}")
def get_actor(source:str, release_year:int):
    # Cargar el archivo CSV en un DataFrame de Pandas
    global df

    # Filtrar por año y plataforma
    filtered_df = df[(df['source'] == source) & (df['release_year'] == release_year)]

    # Contar la cantidad de veces que aparece cada actor en la columna 'cast'
    actor_count = filtered_df['cast'].str.split(',').explode().str.strip().value_counts()

    # Devolver el actor que más se repite
    if actor_count.empty:
        return None
    else:
        return actor_count.index[0]





