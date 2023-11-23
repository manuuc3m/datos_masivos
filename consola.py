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

#Ejemplo de un comando: python3 consola.py --b RECOLETOS --d SALAMANCA
def generar_y_abrir_html1(distrito):

    ruta_de_plantillas = jinja2.FileSystemLoader(searchpath="./plantillas")
    entorno = jinja2.Environment(loader=ruta_de_plantillas)
    nombre_archivo_resultante = "resultado.html"
    template = entorno.get_template("plantilla1.html")
    path_resultado = "resultado.html"

    # Eliminar el archivo resultado.txt si existe
    if os.path.exists(path_resultado):
        os.remove(path_resultado)

    # Información histórica del distrito
    select_query_distrito = f"""SELECT historia FROM distritos WHERE nombre = '{distrito}';"""
    historia_distrito = consultar(select_query_distrito)[0][0]

    # Información de aparcamientos en el distrito
    select_query_aparcamientos = f"""SELECT * FROM aparcamientos WHERE distrito = '{distrito}';"""
    aparcamientos = consultar(select_query_aparcamientos)
    lista_aparcamientos = [{"id": a[0], "nombre": a[1], "localidad": a[2], "coordenada_x": a[3], "coordenada_y": a[4], "barrio": a[5]} for a in aparcamientos]

    # Datos meteorológicos. query_aemet() por defecto escrapea los datos climaticos de
    # el municipio de Madrid, si se desea otro municipio, se especifica su codigo en formato
    # string como parametro
    # aemet_data_current = query_aemet()

    # Escribe el archivo HTML
    with open(nombre_archivo_resultante, mode="w", encoding="utf-8") as results:
        results.write(template.render(distrito=distrito, historia_distrito=historia_distrito,))
        #datos_aemet=aemet_data_current
        print(f"... wrote {nombre_archivo_resultante}")

    
    webbrowser.open('file://' + os.path.realpath(nombre_archivo_resultante))

def listar_barrios(distrito):    
    query = f"SELECT barrio FROM aparcamientos;"
    barrios = consultar(query)
    for i, barrio in enumerate(barrios):
        print(f"{i + 1}. {barrio[0]}")
    return barrios

def seleccionar_barrio(barrios):
    eleccion = int(input("Si quieres ver información concreta de los barrios del distrito, selecciona el número del barrio: "))
    return barrios[eleccion - 1][0]

def generar_y_abrir_html2(distrito, barrio):

    ruta_de_plantillas = jinja2.FileSystemLoader(searchpath="./plantillas")
    entorno = jinja2.Environment(loader=ruta_de_plantillas)
    nombre_archivo_resultante = "resultado.html"
    template = entorno.get_template("plantilla2.html")
    path_resultado = "resultado.html"

    # Eliminar el archivo resultado.txt si existe
    if os.path.exists(path_resultado):
        os.remove(path_resultado)

    # Aqui se puede crear una funcion para armar la consulta en base a que parametros indican en el comando
    select_query = f"""SELECT * FROM aparcamientos WHERE barrio = '{barrio}';"""
    respuesta = consultar(select_query)

    #Se prepara una lista de diccionarios para pasar a la plantilla
    lista_aparcamientos = []
    for a in respuesta:
        lista_aparcamientos.append({"id":a[0],"nombre":a[1],"localidad":a[2],"coordenada_x":a[3],"coordenada_y":a[4],"barrio":a[5]})



    # Escribe el archivo HTML
    with open(nombre_archivo_resultante, mode="w", encoding="utf-8") as results:
        results.write(template.render(distrito=distrito, barrio=barrio, aparcamientos=lista_aparcamientos))
        #datos_aemet=aemet_data_current
        print(f"... wrote {nombre_archivo_resultante}")

    
    webbrowser.open('file://' + os.path.realpath(nombre_archivo_resultante))
        
        
if __name__ == '__main__':
    distritos = listar_distritos()
    distrito_seleccionado = seleccionar_distrito(distritos)
    #generar_y_abrir_html1(distrito_seleccionado)
    barrios = listar_barrios(distrito_seleccionado)
    barrio_seleccionado = seleccionar_barrio(barrios)
    generar_y_abrir_html2(distrito_seleccionado, barrio_seleccionado)


