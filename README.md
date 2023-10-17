

## 1.  COMANDO PARA CREAR ENTORNO VIRTUAL, Si no usan entorno virtual solo seria comando 2 y 3
python3 -m venv venv
.\venv\Scripts\activate ( para Unix source venv/bin/activate)


## 2 .Comando para instalar las dependencia que estan en el archivo setup.py
pip install -e .


## 3. comando para ejecutar el servidor 
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run 



