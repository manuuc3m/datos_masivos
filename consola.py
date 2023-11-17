import sqlite3
import click
import jinja2
import os
import webbrowser

#Retorna 
def consultar(sqlite_select_Query):
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    cursor.execute(sqlite_select_Query)
    respuesta = cursor.fetchall()
    cursor.close()
    return respuesta

#Ejemplo de un comando: python3 consola.py --b RECOLETOS --d SALAMANCA
@click.command()
@click.option('--d', default='', help='Nombre del distrito. [uno,dos,tres]')
@click.option('--b',help='Nomnre del barrio. [RECOLETOS,ETC,ETC]') 
def consola(d, b):
    """Este programa permite generar archivo HTML a partir de criterios de busqueda."""
    print("Distrito: ",d)
    print("Barrio: ",b)

    ruta_de_plantillas = jinja2.FileSystemLoader(searchpath="./plantillas")
    entorno = jinja2.Environment(loader=ruta_de_plantillas)
    nombre_archivo_resultante = "resultado.html"
    template = entorno.get_template("plantilla.html")
    path_resultado = "resultado.html"

    # Eliminar el archivo resultado.txt si existe
    if os.path.exists(path_resultado):
        os.remove(path_resultado)

    # Aqui se puede crear una funcion para armar la consulta en base a que parametros indican en el comando
    select_query = f"""SELECT * FROM aparcamientos WHERE barrio = '{b}';"""
    respuesta = consultar(select_query)

    #Se prepara una lista de diccionarios para pasar a la plantilla
    lista_aparcamientos = []
    for a in respuesta:
        lista_aparcamientos.append({"id":a[0],"nombre":a[1],"localidad":a[2],"coordenada_x":a[3],"coordenada_y":a[4],"barrio":a[5]})

    # Se escribe el archivo resultado.txt  
    with open(nombre_archivo_resultante, mode="w", encoding="utf-8") as results:
        results.write(template.render(aparcamientos=lista_aparcamientos,titulo="Aparcamientos"))
        print(f"... wrote {nombre_archivo_resultante}")
    
    webbrowser.open('file://' + os.path.realpath(nombre_archivo_resultante))
        
if __name__ == '__main__':
    consola()


