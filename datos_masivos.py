import requests 
import xml.etree.ElementTree as ET
import sqlite3 
from bs4 import BeautifulSoup
import webbrowser
import os

wikipedia_url="https://es.wikipedia.org/wiki/"
aparcamientos_url = "https://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.xml"

#listas auxiliares para diferenciar los casos de extraccion de la informacion historica de cada distrito
#existen casos donde no aparece el apartado historia en wikipedia, y se debe extraer el aspecto de cultura, o los primeros parrafos de la pagina
diccWikipedia = { "Historia": ["Centro","Salamanca","Tetuan","Latina","Arganzuela","Chamartin","Chamberi","Carabanchel","Usera","Moratalaz","Ciudad Lineal","Hortaleza","Villaverde","Villa de Vallecas","Vicalvaro","San Blas-Canillejas","Barajas"], "Orígenes": ["Fuencarral-El Pardo"], "Nada": ["Retiro","Moncloa-Aravaca"], "Cultura":["Puente de Vallecas"]}
lista_distritos=["Arganzuela","Chamartin","Chamberi","Fuencarral-El Pardo","Moncloa-Aravaca","Carabanchel","Usera","Puente de Vallecas","Moratalaz","Ciudad Lineal","Hortaleza","Villaverde","Villa de Vallecas","Vicalvaro","San Blas-Canillejas","Barajas","Centro","Retiro","Salamanca","Tetuan","Latina"]
lista_distritos_especiales=["Centro","Retiro","Salamanca","Tetuan","Latina"] #distritos donde se debe añadir _(Madrid) al final de la url

drop_tabla_aparcamientos = """DROP TABLE IF EXISTS aparcamientos;"""
tabla_aparcamientos = """CREATE TABLE aparcamientos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  localidad TEXT NOT NULL,
  coordenada_x REAL,
  coordenada_y REAL
);"""

#tabla de los distritos con su informacion historica(hay 21)
drop_tabla_distritos="""DROP TABLE IF EXISTS distritos;"""
tabla_distritos="""CREATE TABLE distritos (
  nombre TEXT PRIMARY KEY,
  historia TEXT ,
  consideraciones TEXT
 );"""



 #INIT

def init_db():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("conexion exitosa")
        cursor.execute(drop_tabla_aparcamientos)
        cursor.execute(tabla_aparcamientos)
        cursor.execute(drop_tabla_distritos)
        cursor.execute(tabla_distritos)
        cursor.close()

    except sqlite3.Error as error:
        print("Error base  de dato ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("conexion cerrada")



#METODOS PARA OBTENER APARCAMIENTOS

def cargar_dato_aparcamientos(nombre, localidad, coordenada_x, coordenada_y):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        count = cursor.execute("""INSERT INTO aparcamientos (nombre, localidad, coordenada_x, coordenada_y) VALUES (?, ?, ?, ?)""", (nombre, localidad, coordenada_x, coordenada_y))
        sqliteConnection.commit()
        print("agregado ", cursor.rowcount)

    except sqlite3.Error as error:
        print("Error conectando", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Cerrar conexion")


def extraer_datos_aparcamientos(url):
    r = requests.get(url)
    root = ET.fromstring(r.content)
    return root


def tranformar_datos_aparcamientos(data):
    datos_transformados = []
    for contenido in data.findall('contenido'):
        objeto = {}
        for atributo in contenido.iter('atributo'):
            NOMBRE = atributo.attrib['nombre']
            if(NOMBRE == 'NOMBRE' or NOMBRE == 'LOCALIDAD' or NOMBRE == 'COORDENADA-X' or NOMBRE == 'COORDENADA-Y'):
                objeto[NOMBRE] = atributo.text
        datos_transformados.append(objeto)
    return datos_transformados


def cargar_datos_aparcamientos(datos):
    for dato in datos:
        cargar_dato_aparcamientos(dato['NOMBRE'], dato['LOCALIDAD'], dato['COORDENADA-X'], dato['COORDENADA-Y'])



#METODOS PARA OBTENER INFORMACION HISTORICA POR CADA DISTRITO

def extraer_distritos():

    for i in lista_distritos:
        
        if(i in lista_distritos_especiales):
            url = wikipedia_url + i + "_(Madrid)"
        else:
            url = wikipedia_url + i
        print('\n\n'+ url + '\n\n')
        resp=requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        if (i in diccWikipedia["Historia"]):
            scraping('Historia',soup)

        elif(i in diccWikipedia["Orígenes"]):
            scraping('Orígenes',soup)

        elif(i in diccWikipedia["Nada"]):
            scraping('Nada',soup)

        else:
            scraping('Cultura',soup)



def scraping(inicio,soup):

    if (inicio=='Nada'):
        titulo = soup.find('table', {'class': 'infobox geography vcard'})
    else:
        titulo = soup.find('span', {'id': inicio})

    if titulo:
        contenido = []

        for elemento in titulo.find_all_next(['p', 'h2']):
            if elemento.name == 'h2':
                break  
            contenido.append(elemento.get_text(strip=True))

        print('\n'.join(contenido))

# Función para mostrar los distritos y capturar la elección del usuario
def mostrar_menu_distritos():
    print("En qué distrito quieres ver la ruta:")
    for i, distrito in enumerate(lista_distritos, start=1):
        print(f"{i}. {distrito}")
    eleccion = int(input("Elige un número: "))
    return lista_distritos[eleccion - 1]




#METODO PRINCIPAL MAIN
if __name__ == '__main__':
    print(aparcamientos_url)
    init_db()
    extraer_distritos()
    data = extraer_datos_aparcamientos(aparcamientos_url)
    datos = tranformar_datos_aparcamientos(data)
    cargar_datos_aparcamientos(datos)
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = "SELECT * from aparcamientos"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("Registros", record)
    cursor.close()     
    distrito_seleccionado = mostrar_menu_distritos()
    print(f"Has seleccionado: {distrito_seleccionado}")    
    webbrowser.open('file://' + os.path.realpath("C:\\Users\\datosmasivos\\Source\\Repos\\datos_masivos\\vista1.html"))




    

    