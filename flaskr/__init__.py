import os
from flask import Flask,render_template

def create_app(test_config=None):

    # Crear la aplicacion y configura el app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # Ruta de Hola mundo
    @app.route('/hola')
    def hello():
        return 'Hola, Mundo!'
        
    #Ruta de index    
    @app.route('/index')
    def index():
        return render_template('index.html') 

    # Ejemplo para crear modulo en flask con blueprints
    from . import modulo
    app.register_blueprint(modulo.bp)
    app.add_url_rule('/', endpoint='index')

    return app


