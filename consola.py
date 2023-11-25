import sqlite3
import click
import jinja2
import os
import webbrowser

#IMPORTAR AEMET MEDIADOR
from aemet_mediador import query_aemet

#Retorna 
def consultar(sqlite_select_Query):
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_select_Query)
    respuesta = cursor.fetchall()
    cursor.close()
    return respuesta

def listar_distritos():
    query = "SELECT nombre FROM distritos"
    distritos = consultar(query)
    for i, distrito in enumerate(distritos):
        print(f"{i + 1}. {distrito[0]}")
    return distritos

def seleccionar_distrito(distritos):
    eleccion = int(input("Selecciona el número del distrito: "))
    return distritos[eleccion - 1][0]

def generar_y_abrir_html(distrito):

    ruta_de_plantillas = jinja2.FileSystemLoader(searchpath="./plantillas")
    entorno = jinja2.Environment(loader=ruta_de_plantillas)
    nombre_archivo_resultante = "resultado.html"
    template = entorno.get_template("plantilla.html")
    path_resultado = "resultado.html"

    # Eliminar el archivo resultado.txt si existe
    if os.path.exists(path_resultado):
        os.remove(path_resultado)    
    
    #Informacion de rutas en el distrito 
    select_query_rutas = f"""SELECT * FROM rutas WHERE distrito = '{distrito}';"""
    rutas = consultar(select_query_rutas)
    lista_rutas = [{"nombre": r[0], "distrito": r[1], "distancia": r[2], "tiempo": r[3], "dificultad": r[4], "tipo_ruta": r[5], "descripcion": r[6], "trailrank": r[7], "des_pos": r[8], "des_neg": r[9], "alt_max": r[10], "alt_min": r[11],} for r in rutas]

    # Información histórica del distrito
    select_query_distrito = f"""SELECT historia FROM distritos WHERE nombre = '{distrito}';"""
    historia_distrito = consultar(select_query_distrito)[0][0]
           
    # Información de aparcamientos en el distrito
    select_query_aparcamientos = f"""SELECT * FROM aparcamientos WHERE distrito = '{distrito.upper()}';"""
    aparcamientos = consultar(select_query_aparcamientos)
    lista_aparcamientos = [{"id": a[0], "nombre": a[1], "localidad": a[2], "coordenada_x": a[3], "coordenada_y": a[4], "barrio": a[5], "distrito": a[6]} for a in aparcamientos]

    # Datos meteorológicos. query_aemet() por defecto escrapea los datos climaticos de
    # el municipio de Madrid, si se desea otro municipio, se especifica su codigo en formato
    # string como parametro
    aemet_data_current = query_aemet()


    # Escribe el archivo HTML
    with open(nombre_archivo_resultante, mode="w", encoding="utf-8") as results:
        results.write(template.render(
            distrito=distrito,
            rutas=lista_rutas,
            historia_distrito=historia_distrito ,     
            datos_aemet=aemet_data_current,
            aparcamientos=lista_aparcamientos
        ))        
        print(f"... wrote {nombre_archivo_resultante}")
    
    webbrowser.open('file://' + os.path.realpath(nombre_archivo_resultante))
           
        
if __name__ == '__main__':
    distritos = listar_distritos()
    distrito_seleccionado = seleccionar_distrito(distritos)
    generar_y_abrir_html(distrito_seleccionado)


