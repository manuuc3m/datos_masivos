import requests 
import xml.etree.ElementTree as ET
import sqlite3 

aparcamientos_url = 'https://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.xml'

drop = """DROP TABLE IF EXISTS sitios;"""
tabla_sitios = """CREATE TABLE sitios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  localidad TEXT NOT NULL,
  coordenada_x REAL,
  coordenada_y REAL
);"""

def cargar_dato(nombre, localidad, coordenada_x, coordenada_y):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        count = cursor.execute("""INSERT INTO sitios (nombre, localidad, coordenada_x, coordenada_y) VALUES (?, ?, ?, ?)""", (nombre, localidad, coordenada_x, coordenada_y))
        sqliteConnection.commit()
        print("agregado ", cursor.rowcount)

    except sqlite3.Error as error:
        print("Error conectando", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Cerrar conexion")

def init_db():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("conexion exitosa")
        cursor.execute(drop)
        cursor.execute(tabla_sitios)
        cursor.close()

    except sqlite3.Error as error:
        print("Error base  de dato ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("conexion cerrada")

def extraer_datos(url):
    r = requests.get(url)
    root = ET.fromstring(r.content)
    return root

def tranformar_datos(data):
    datos_transformados = []
    for contenido in data.findall('contenido'):
        objeto = {}
        for atributo in contenido.iter('atributo'):
            NOMBRE = atributo.attrib['nombre']
            if(NOMBRE == 'NOMBRE' or NOMBRE == 'LOCALIDAD' or NOMBRE == 'COORDENADA-X' or NOMBRE == 'COORDENADA-Y'):
                objeto[NOMBRE] = atributo.text
        datos_transformados.append(objeto)
    return datos_transformados

def cargar_datos(datos):
    for dato in datos:
        cargar_dato(dato['NOMBRE'], dato['LOCALIDAD'], dato['COORDENADA-X'], dato['COORDENADA-Y'])

if __name__ == '__main__':
    print(aparcamientos_url)
    init_db()
    data = extraer_datos(aparcamientos_url)
    datos = tranformar_datos(data)
    cargar_datos(datos)
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = "SELECT * from sitios"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("Registros", record)
    cursor.close()


    

    