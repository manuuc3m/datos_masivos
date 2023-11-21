def refine_precipitacion(data):
    return [f"{e['value']} %" for e in data]

def refine_nieve(nievedata):
    values = [e['value'] for e in nievedata]
    print(values)
    mapping_empties = [ '0 %' if e == '' else f"{e} %" for e in values]
    return mapping_empties

def refine_nubosidad(nubosdata):
    descriptions = [e['descripcion'] if e != '' else 'Despejado' for e in nubosdata]
    return descriptions

wind_directions = {
    'N': 'Norte',
    'S': 'Sur',
    'E': 'Este',
    'O': 'Oeste',
    'NE': 'Noreste',
    'SE': 'Sureste',
    'NO': 'Noroeste',
    'SO': 'Suroeste'
}

def refine_viento(vientodata):
    info = [
        {
            'direccion': 'No hay dirección' if e['direccion'] == '' else wind_directions[e['direccion']],
            'velocidad': f"{e['velocidad']} Km/h"
        } for e in vientodata
    ]
    return info