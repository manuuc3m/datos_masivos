## Para ejecuatar estos comando debe estar en la carpeta del repositorioa datos_masivos
## y tener instaldos Python

## Sin no usa entorno virtual, solo es necesario Paso 2 y Paso 3

## 1.  COMANDO PARA CREAR ENTORNO VIRTUAL, Si no usan entorno virtual solo seria comando 2 y 3
python3 -m venv venv
.\venv\Scripts\activate ( para Unix source venv/bin/activate)


## 2 .Comando para instalar las dependencia que estan en el archivo setup.py
pip install -e . ( o si tiene la version 3: pip3 install -e .)


## 3. comando para ejecutar el servidor 
export FLASK_APP=flaskr
flask run 

## 4. WINDOWS
# ./flaskr is flask directory, is a relativa path
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
flask run 



