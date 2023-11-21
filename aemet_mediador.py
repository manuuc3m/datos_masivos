import requests
from datetime import datetime
ENDPOINT = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDAzNjM4ODVAYWx1bW5vcy51YzNtLmVzIiwianRpIjoiMDNiNWMyZTYtMTAxZC00ZDllLWFmMjUtMzQ3NDNlODY0Nzc4IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3MDA1MDQ1NzcsInVzZXJJZCI6IjAzYjVjMmU2LTEwMWQtNGQ5ZS1hZjI1LTM0NzQzZTg2NDc3OCIsInJvbGUiOiIifQ.s0tV1bkizW0ZQtxR97rbelca3ISYrD3fAMF-WO8S8Hc"

def query_aemet(citycode = '28079'): 
    # Set url with code
    url = ENDPOINT + citycode
    # Set params
    params = {
        'api_key': API_KEY
    }
    # Realiza la solicitud GET
    response = requests.get(url, params=params)

    # Verifica que la solicitud fue exitosa
    if response.status_code == 200:
        # Procesa la respuesta
        data = response.json()
        print('FIRST API CALL')
        # print(data)
        sub_query_data(data['datos'])
    else:
        print("Error en la solicitud:", response.status_code)


def sub_query_data(data_route):
    response = requests.get(data_route)
    if response.status_code != 200:
        print("La consulta de los datos meteorologicos ha FALLADO")
        return {}
    print('DATOS METEOROLOGICOS DE HOY POR AEMET')
    # print(response.json())
    meteorogical_data = response.json()
    refined_data(meteorogical_data[0])

def refined_data(data):
    print('REFINANDO DATOS')
    prediccion_semanal = data['prediccion']['dia']
    # Prediccion semanal contiene los valores de los sietes dias.
    
    # Dia de la semana actual
    week_day = datetime.now().weekday()
    prediccion_de_hoy = prediccion_semanal[week_day]
    
    #hora actual
    hora_actual = datetime.now().hour + round(datetime.now().minute / 60, 2)

    #periodo actual
    periodo = 0
    if 0 <= hora_actual <= 6:
        periodo = 0
    if 6 < hora_actual <= 12:
        periodo = 1
    if 12 < hora_actual <= 18:
        periodo = 2
    if 18 < hora_actual <= 24:
        periodo = 3
    
    
    refined_data = {}
    refined_data['periodo_actual'] = periodo
    refined_data['periodos'] = ['00:00 - 06:00', '06:00 - 12:00', '12:00 - 18:00', '18:00 - 24:00']

    refined_data['probabilidad_precipitacion'] = prediccion_semanal['probPrecipitacion'][3:]
    refined_data['probabilidad_nieve'] = prediccion_semanal['cotaNieveProv'][3:]
    refined_data['nubosidad'] = prediccion_semanal['estadoCielo'][3:]
    refined_data['viento'] = prediccion_semanal['viento'][3:]
    refined_data['temperatura'] = prediccion_semanal['temperatura']
    
    return refined_data


query_aemet()