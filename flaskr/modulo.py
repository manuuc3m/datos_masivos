from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

bp = Blueprint('modulo', __name__, url_prefix='/modulo')

@bp.route('/ruta',methods=['GET'])
def create():
    return render_template('modulo/pagina.html')

#Aqui se puede crear ruta que retorne un json, un html o lo que sea necesario para el modulo
