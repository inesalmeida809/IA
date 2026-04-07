from ...data.cities_graph import cidades_vizinhas
from .calcular_heuristica import calcular_heuristica

def procura_sofrega(cidade_origem, cidade_destino):
    caminho = [cidade_origem]
    cidade_atual = cidade_origem
    distancia = 0

    print(f"A iniciar procura sofrega de {cidade_origem} para {cidade_destino}")

    while cidade_atual != cidade_destino:
        proximos_nos = cidades_vizinhas.get(cidade_atual, {})

        if not  proximos_nos:
            print("Caminho não encontrado.(Sem saída)")
            return None
        
        proxima_cidade = min(proximos_nos, key=lambda cidade: calcular_heuristica(cidade, cidade_destino))
        distancia += proximos_nos[proxima_cidade]
 
        h_val = calcular_heuristica(proxima_cidade, cidade_destino)
        print(f"Interação: De {cidade_atual} escolhi {proxima_cidade} (Heurística: {h_val:.2f})")

        cidade_atual = proxima_cidade
        caminho.append(cidade_atual)
    print(f"\nCaminho final: {caminho}")
    print(f"Distância: {distancia}")
    return caminho


if __name__ == "__main__":
    origem = "Coimbra"
    destino = "Faro"
    caminho_encontrado = procura_sofrega(origem, destino)