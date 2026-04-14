import os
import json
from llama_cpp import Llama

pasta_llm_logic = os.path.dirname(os.path.abspath(__file__))
pasta_llm = os.path.dirname(pasta_llm_logic)
pasta_modelo = os.path.join(pasta_llm, "model_IA")

ficheiro_model = "Qwen2.5-3B-Instruct-Q4_K_M.gguf"
caminho_completo = os.path.join(pasta_modelo, ficheiro_model)

def iniciar_modelo():
    if not os.path.exists(caminho_completo):
        print("\n\nErro: O modelo não foi encontrado.")
        return

    print("\n\nA carregar o modelo...")
    
    llm = Llama(
        model_path=caminho_completo,
        n_ctx=1024, 
        n_gpu_layers=-1, 
        n_threads=6,
        verbose=False
    )

    return llm