import requests 
import xml.etree.ElementTree as ET
import sqlite3 
from bs4 import BeautifulSoup
import webbrowser
import os
import re
import time

wikipedia_url="https://es.wikipedia.org/wiki/"
aparcamientos_url = "https://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.xml"

#listas auxiliares para diferenciar los casos de extraccion de la informacion historica de cada distrito
#existen casos donde no aparece el apartado historia en wikipedia, y se debe extraer el aspecto de cultura, o los primeros parrafos de la pagina
diccWikipedia = { "Historia": ["Centro","Salamanca","Tetuan","Latina","Arganzuela","Chamartin","Chamberi","Carabanchel","Usera","Moratalaz","Ciudad Lineal","Hortaleza","Villaverde","Villa de Vallecas","Vicalvaro","San Blas-Canillejas","Barajas"], "Orígenes": ["Fuencarral-El Pardo"], "Nada": ["Retiro","Moncloa-Aravaca"], "Cultura":["Puente de Vallecas"]}
lista_distritos=["Arganzuela","Chamartin","Chamberi","Fuencarral-El Pardo","Moncloa-Aravaca","Carabanchel","Usera","Puente de Vallecas","Moratalaz","Ciudad Lineal","Hortaleza","Villaverde","Villa de Vallecas","Vicalvaro","San Blas-Canillejas","Barajas","Centro","Retiro","Salamanca","Tetuan","Latina"]
lista_distritos_especiales=["Centro","Retiro","Salamanca","Tetuan","Latina"] #distritos donde se debe añadir _(Madrid) al final de la url

# Diccionario clave-valor para mantener consistencia entre distritos
diccWikiloc = {"Arganzuela" : ["arganzuela"],"Chamartin" : ["chamartin-de-la-rosa"],"Chamberi" : ["chamberi"], "Fuencarral-El Pardo" : ["fuencarral-el-pardo"],
"Moncloa-Aravaca" : ["moncloa", "aravaca"], "Carabanchel" : ["carabanchel"],"Usera" : ["usera"], "Puente de Vallecas" : ["puente-de-vallecas"],
"Moratalaz" : ["moratalaz"], "Ciudad Lineal" : ["ciudad-lineal"], "Hortaleza" : ["hortaleza"], "Villaverde" : ["villaverde"], "Villa de Vallecas" : ["villa-de-vallecas"],
"Vicalvaro" : ["vicalvaro"], "San Blas-Canillejas" : ["san-blas", "canillejas"], "Barajas" : ["barajas-de-madrid"],"Centro" : ["centro"],
"Retiro" : ["retiro"], "Salamanca" : ["salamanca"], "Tetuan" : ["tetuan-de-las-victorias"], "Latina" : ["la-latina"]}

# Cabeceras generales
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", }


drop_tabla_aparcamientos = """DROP TABLE IF EXISTS aparcamientos;"""
tabla_aparcamientos = """CREATE TABLE aparcamientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    localidad TEXT NOT NULL,
    coordenada_x REAL,
    coordenada_y REAL,
    barrio TEXT,
    distrito TEXT
);"""

#tabla de los distritos con su informacion historica(hay 21)
drop_tabla_distritos="""DROP TABLE IF EXISTS distritos;"""
tabla_distritos="""CREATE TABLE distritos (
  nombre TEXT PRIMARY KEY,
  historia TEXT NOT NULL
 );"""

 #tabla con las rutas, cada una tiene el distrito al que pertenece
drop_tabla_rutas = """DROP TABLE IF EXISTS rutas;"""
tabla_rutas = """CREATE TABLE rutas (
    nombre TEXT PRIMARY KEY,
    distrito TEXT NOT NULL,
    distancia TEXT NOT NULL,
    tiempo TEXT NOT NULL,
    dificultad TEXT NOT NULL,
    tipo_ruta TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    trailrank INTEGER,
    des_pos TEXT NOT NULL,
    des_neg TEXT NOT NULL,
    alt_max TEXT NOT NULL,
    alt_min TEXT NOT NULL
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
        cursor.execute(drop_tabla_rutas)
        cursor.execute(tabla_rutas)
        cursor.close()

    except sqlite3.Error as error:
        print("Error base  de dato ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("conexion cerrada")



#METODOS PARA OBTENER APARCAMIENTOS

def cargar_dato_aparcamientos(nombre, localidad, coordenada_x, coordenada_y,barrio,distrito):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        count = cursor.execute("""INSERT INTO aparcamientos (nombre, localidad, coordenada_x, coordenada_y,barrio,distrito) VALUES (?, ?, ?, ?, ?, ?)""", (nombre, localidad, coordenada_x, coordenada_y,barrio,distrito))
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
            #print(NOMBRE)
            if(NOMBRE == 'NOMBRE' or NOMBRE == 'LOCALIDAD' or NOMBRE == 'COORDENADA-X' or NOMBRE == 'COORDENADA-Y' or NOMBRE == 'BARRIO' or NOMBRE == 'DISTRITO'):
                objeto[NOMBRE] = atributo.text
        datos_transformados.append(objeto)
    return datos_transformados


def cargar_datos_aparcamientos(datos):
    for dato in datos:
        cargar_dato_aparcamientos(dato['NOMBRE'], dato['LOCALIDAD'], dato['COORDENADA-X'], dato['COORDENADA-Y'], dato['BARRIO'], dato['DISTRITO'])



#METODOS PARA OBTENER INFORMACION HISTORICA POR CADA DISTRITO

def extraer_distritos():

    for i in lista_distritos:
        
        if(i in lista_distritos_especiales):
            url = wikipedia_url + i + "_(Madrid)"
        else:
            url = wikipedia_url + i
        print(url)
        resp=requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        if (i in diccWikipedia["Historia"]):
            info = scraping('Historia',soup)

        elif(i in diccWikipedia["Orígenes"]):
            info = scraping('Orígenes',soup)

        elif(i in diccWikipedia["Nada"]):
            info = scraping('Nada',soup)

        else:
            info = scraping('Cultura',soup)

        cargar_info_distritos(i,info)


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
            contenido.append(elemento.get_text(strip=False))
        texto = ' \n'.join(contenido)
        texto_limpiado = limpieza(texto)
        #print(texto_limpiado)
        return texto_limpiado


def limpieza(texto):
    patron_referencias = r'(?:\(|\[)([0-9]{1,2})(?:\)|\])' #eliminar corchetes y parentesis de referencias de wikipedia

    # Reemplazar las referencias con una cadena vacía
    texto_limpio = re.sub(patron_referencias, '', texto)

    return texto_limpio



def cargar_info_distritos(distrito,texto):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        count = cursor.execute("""INSERT INTO distritos (nombre, historia) VALUES (?, ?)""", (distrito, texto))
        sqliteConnection.commit()

    except sqlite3.Error as error:
        print("Error conectando", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


            
#METODOS PARA OBTENER RUTAS DE SENDERISMO POR CADA DISTRITO

def extraer_rutas_senderismo():
    for distrito in lista_distritos:
        extraer_rutas_distrito(distrito)
        time.sleep(5)

def extraer_rutas_distrito(distrito):

    #Extraer info de un distrito
    for subdistrito in diccWikiloc[distrito]:
        distrito_url = "https://es.wikiloc.com/rutas/senderismo/espana/comunidad-de-madrid/" + subdistrito
        resp_distrito = requests.get(distrito_url, headers=headers)
        soupDistrito = BeautifulSoup(resp_distrito.text, 'html.parser')

        #Extraer links de las rutas del distrito
        lista_links_rutas = []
        nombreRutas = soupDistrito.find_all('h2', {'class': 'trail__title'})
        for ruta in nombreRutas:
            lista_links_rutas.append(ruta.findChild("a")['href'])

        for i in range(10):
            extraer_info_ruta(lista_links_rutas[i], distrito)

def extraer_info_ruta(url, distrito):

   # Extraer info de una ruta
    ruta_url = "https://es.wikiloc.com/" + url
    resp_ruta = requests.get(ruta_url, headers=headers)
    soupRuta = BeautifulSoup(resp_ruta.text, 'html.parser')

    # Encontrar nombre
    nombre_ruta_element = soupRuta.find('div', {'class': 'view__header__title'})
    nombre = nombre_ruta_element.text.strip()

    # Encontrar info principal
    info_element = soupRuta.find_all('div', {'class': 'd-item'})
    info = []

    for i in range(9):
        if i != 5:
            info.append(info_element[i].text.strip().replace("\xa0", " ").splitlines()[1])
        else:
            trailrank_texts = info_element[5].text.strip().split()
            hasStar = 0
            if len(trailrank_texts) == 3:
                hasStar = 1
            info.append(info_element[5].text.strip().split()[1 + hasStar])

    distancia = info[0]
    des_pos = info[1]
    dificultad = info[2]
    des_neg = info[3]
    alt_max = info[4]
    trailrank = info[5]
    alt_min = info[6]
    tipo_ruta = info[7]
    tiempo = info[8]

    # Encontrar descripción
    descripcion_element = soupRuta.find('div', {'class': 'description dont-break-out'})
    if (descripcion_element == None):
        descripcion_element = soupRuta.find('div', {'class': 'description dont-break-out description-original'})
    if (descripcion_element != None):
        html_desc = str(descripcion_element)
        descripcion = filter_description(html_desc)
    else:
        descripcion = "No hay descripcion para esta ruta"

    cargar_datos_rutas(nombre, distrito, distancia, tiempo, dificultad, tipo_ruta, descripcion, trailrank, des_pos, des_neg, alt_max, alt_min)


#Método para obtener solo el texto sin formato de la descripción
def filter_description(text):

    filter_text = text.replace("<br/>", "\n")
    text_filtered = ""
    shouldWrite = True

    for c in filter_text:
        if c == '<':
            shouldWrite = False
        if shouldWrite:
            text_filtered += c
        if c == '>':
            shouldWrite = True
    return text_filtered.strip()   

def cargar_datos_rutas(nombre, distrito, distancia, tiempo, dificultad, tipo_ruta, descripcion, trailrank, des_pos, des_neg, alt_max, alt_min):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        count = cursor.execute(
            """INSERT INTO rutas (nombre, distrito, distancia, tiempo, dificultad, tipo_ruta, descripcion, trailrank, des_pos, des_neg, alt_max, alt_min) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,?)""",
            (nombre, distrito, distancia, tiempo, dificultad, tipo_ruta, descripcion, trailrank, des_pos, des_neg, alt_max, alt_min))
        sqliteConnection.commit()
        print("agregado", cursor.rowcount)

    except sqlite3.Error as error:
        print("Error conectando", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


           

#METODO PRINCIPAL MAIN
if __name__ == '__main__':
    print(aparcamientos_url)
    init_db()
    extraer_distritos()
    extraer_rutas_senderismo()
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    query_distritos = "SELECT * from distritos"
    distritos= cursor.execute(query_distritos)
    #distritos = cursor.fetchall()
    for i in distritos:
        print(i)
        print("\n\n\n\n\n\n")
    cursor.close()     
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
    



    

    