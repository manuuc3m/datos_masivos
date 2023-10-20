from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

bp = Blueprint('modulowikiloc', __name__, url_prefix='/modulowikiloc')


#Aqui se puede crear ruta que retorne un json, un html o lo que sea necesario para el modulo
@bp.route('/<cityname>/fonts/', methods=['GET'])
def getCityFonts(cityname=''):
    return { 'data': 'PROOF FROM STARTING API', 'city': cityname}