#Aqui temos a função responsável por calcular a distância em linha reta de uma cidade à outra através das suas coordenadas

import math

from ...data.city_coordinates import coordenadas

def calcular_heuristica(cidade_atual, cidade_destino):
    lat1, lon1 = coordenadas[cidade_atual]
    lat2, lon2 = coordenadas[cidade_destino]

    R = 6371.0  # Raio médio da Terra em quilómetros
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Aplicação da Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia_km = R * c
   
    return distancia_km