import requests
from datetime import datetime
ENDPOINT = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDAzNjM4ODVAYWx1bW5vcy51YzNtLmVzIiwianRpIjoiMDNiNWMyZTYtMTAxZC00ZDllLWFmMjUtMzQ3NDNlODY0Nzc4IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3MDA1MDQ1NzcsInVzZXJJZCI6IjAzYjVjMmU2LTEwMWQtNGQ5ZS1hZjI1LTM0NzQzZTg2NDc3OCIsInJvbGUiOiIifQ.s0tV1bkizW0ZQtxR97rbelca3ISYrD3fAMF-WO8S8Hc"


#Importar funciones auxiliares
import aemet_adhoc_refiners as ref

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
        # print('FIRST API CALL')
        # print(data)
        return sub_query_data(data['datos'])
    else:
        return {
            'status': '400',
            'message': 'Ocurrio un error durante la recuperacion de datos meteorologicos'
        }


def sub_query_data(data_route):
    response = requests.get(data_route)
    if response.status_code != 200:
        return {
            'status': 400,
            'message': 'Ocurrio un error durante la recuperacion de datos meteorologicos'
        }
    # print('DATOS METEOROLOGICOS DE HOY POR AEMET')
    # print(response.json())
    meteorogical_data = response.json()
    return refined_data(meteorogical_data[0])




def refined_data(data):
    # print('REFINANDO DATOS')
    prediccion_de_hoy = data['prediccion']['dia']
    # Prediccion semanal contiene los valores de los sietes dias.

    # Dia de la semana actual
    week_day = datetime.now().weekday()
    prediccion_de_hoy = prediccion_de_hoy[week_day]

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

    refined_data['probabilidad_precipitacion'] = ref.refine_precipitacion(prediccion_de_hoy['probPrecipitacion'][3:])
    refined_data['probabilidad_nieve'] = ref.refine_nieve(prediccion_de_hoy['cotaNieveProv'][3:])
    refined_data['nubosidad'] = ref.refine_nubosidad(prediccion_de_hoy['estadoCielo'][3:])
    refined_data['viento'] = ref.refine_viento(prediccion_de_hoy['viento'][3:])
    refined_data['temperatura'] = prediccion_de_hoy['temperatura']
    # Cada unos de estos campos tienen mucha basura que en el frontend no va a hacer falta
    # Asi que se tienen que eliminar con funciones adhoc, no hay de otra

    refined_data['status'] = 200
    return refined_data




query_aemet()