import os
import sys

from huggingface_hub import hf_hub_download

pasta_llm_logic = os.path.dirname(os.path.abspath(__file__))
pasta_llm = os.path.dirname(pasta_llm_logic)
pasta_modelo = os.path.join(pasta_llm, "model_IA")

ficheiro_model = "Qwen2.5-3B-Instruct-Q4_K_M.gguf"
caminho_completo = os.path.join(pasta_modelo, ficheiro_model)


def verificar_instalar_modelo():
    if not os.path.exists(caminho_completo):
        print(f"\n\nATENÇÃO: O modelo '{ficheiro_model}' não foi encontrado na tua máquina.")
        
        resposta = input("Desejas fazer o download do modelo agora? (~2.2 GB) (s/n): ").strip().lower()

        if resposta == 's':
            print("A iniciar o download... (Isto pode demorar alguns minutos dependendo da internet)")

            try:
                hf_hub_download(
                        repo_id="bartowski/Qwen2.5-3B-Instruct-GGUF", 
                        filename=ficheiro_model, 
                        local_dir=pasta_modelo
                )
                print("Download concluído com sucesso!\n")
            except Exception as e:
                print(f"\n\nOcorreu um erro durante o download: {e}")
                sys.exit(1)
                
        else:
            print("\n\nOperação cancelada. O servidor não vai conseguir iniciar sem o modelo.")
