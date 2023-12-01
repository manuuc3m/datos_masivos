def refine_precipitacion(data):
    precipitationData = [f"{e['value']} %" for e in data]
    if ( len(precipitationData) < 7):
        diff = ['0 %']*(7 - len(precipitationData))
        return precipitationData + diff
    return precipitationData

def refine_nieve(nievedata):
    values = [e['value'] for e in nievedata]
    print('values', values)
    mapping_empties = [ 'Sin nieve' if e == '' else f"{e} m" for e in values]
    # Necesario que sean siempre 7 valores
    if (len(mapping_empties) < 7):
        diff = ['Sin nieve'] * ( 7 - len(mapping_empties) )
        return mapping_empties + diff
    return mapping_empties

def refine_nubosidad(nubosdata):
    descriptions = [e['descripcion'] if e != '' else 'Despejado' for e in nubosdata]
    if (len(descriptions) < 7):
        diff = ['Sin nubes'] * ( 7 - len(descriptions) )
        return descriptions + diff
    return descriptions

wind_directions = {
    'N': 'Norte',
    'S': 'Sur',
    'E': 'Este',
    'O': 'Oeste',
    'NE': 'Noreste',
    'SE': 'Sureste',
    'NO': 'Noroeste',
    'SO': 'Suroeste',
    'C': 'No hay viento'
}

def refine_viento(vientodata):
    info = [
        {
            'direccion': 'No hay viento' if e['direccion'] == '' else wind_directions[e['direccion']],
            'velocidad': f"{e['velocidad']} Km/h"
        } for e in vientodata
    ]
    if (len(info) < 7):
        diff = [{'direccion': 'No hay viento', 'velocidad': '0 Km/h'}] * ( 7 - len(info) )
        return info + diff
    return info