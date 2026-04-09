from algorithms.custo_uniforme import custo_uniforme

def custo_uniforme_service(chegada, destino):
    caminho, custo = custo_uniforme(chegada, destino)
    
    if caminho is not None and custo is not None:
        return {
            "caminho": caminho,
            "custo": custo,
        }
    else:
        return {
            "erro": "Nenhum caminho encontrado"
        }