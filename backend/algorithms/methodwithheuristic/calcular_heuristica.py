#Aqui temos a função responsável por calcular a distância em linha reta de uma cidade à outra através das suas coordenadas

import math
from ...data.city_coordinates import coordenadas

def calcular_heuristica(cidade_atual, cidade_destino):
    lat1, lon1 = coordenadas[cidade_atual]
    lat2, lon2 = coordenadas[cidade_destino]

    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)