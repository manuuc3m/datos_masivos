import requests 
import xml.etree.ElementTree as ET
import sqlite3 

wikipedia_url="https://es.wikipedia.org/wiki/"
wikipedia_distritos_url="https://es.wikipedia.org/wiki/Anexo:Distritos_de_Madrid"
aparcamientos_url = "https://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.xml"

lista_rutas=["Argüelles","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",]

drop_tabla_aparcamientos = """DROP TABLE IF EXISTS aparcamientos;"""
tabla_aparcamientos = """CREATE TABLE aparcamientos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  localidad TEXT NOT NULL,
  coordenada_x REAL,
  coordenada_y REAL
);"""

#tabla de la informacion historica de los distritos (hay 21)
drop_tabla_info="""DROP TABLE IF EXISTS info_historica;"""
tabla_info_historica="""CREATE TABLE info_historica (
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
        cursor.execute(drop_tabla_info)
        cursor.execute(tabla_info_historica)
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



#METODOS PARA OBTENER INFORMACION HISTORICA

def poblar



#METODO PRINCIPAL MAIN

if __name__ == '__main__':
    print(aparcamientos_url)
    init_db()
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


    

    