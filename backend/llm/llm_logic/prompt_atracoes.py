import os
import json

pasta_llm_logic = os.path.dirname(os.path.abspath(__file__))
ficheiro_dados = os.path.join(pasta_llm_logic, "monumentos.json")

def carregar_dados_monumentos():
    if not os.path.exists(ficheiro_dados):
        print("\n\nErro: Ficheiro monumentos.json não encontrado.")
        return {}
    
    with open(ficheiro_dados, "r", encoding="utf-8") as f:
        return json.load(f)

def atracoes_monumentos_stream(llm, distritos_a_testar):

    base_dados = carregar_dados_monumentos()

    json_monumentos = []

    for distrito in distritos_a_testar:
        informacao_real = base_dados.get(distrito.capitalize(), None)

        if not informacao_real:
            yield json.dumps({"erro": f"Não temos dados no ficheiro para o distrito: {distrito}"}) + "\n"
            continue

        messages = [
            {
                "role": "system", 
                "content": "És um assistente turístico especializado em Portugal. A tua única função é processar os dados fornecidos e retornar o resultado EXCLUSIVAMENTE em formato JSON válido. Não escrevas nenhuma saudação, nem texto adicional antes ou depois do JSON."
            },
            {
                "role": "user", 
                "content": f"""As 3 atrações do distrito de {distrito} são estas:
                {informacao_real}

                Apresenta estas atrações e escreve uma frase curta e factual a descrever cada uma delas. 
                Devolve a resposta ESTRITAMENTE neste formato JSON:
                {{
                "distrito": "{distrito}",
                "atracoes": [
                    {{
                    "nome": "Nome da Atração",
                    "descricao": "Descrição curta e factual gerada por ti."
                    }}
                ]
                }}"""
            }
        ]

        print(f"A perguntar pelos monumentos de {distrito} usando o ficheiro JSON...\n")

        resposta = llm.create_chat_completion(
            messages=messages,
            max_tokens=400,   
            temperature=0.1,  
            top_p=0.9,
            repeat_penalty=1.1
        )

        texto_gerado = resposta['choices'][0]['message']['content'].strip()
        if texto_gerado.startswith("```json"):
            texto_gerado = texto_gerado.replace("```json", "", 1).replace("```", "", 1).strip()
        elif texto_gerado.startswith("```"):
            texto_gerado = texto_gerado.replace("```", "", 1).replace("```", "", 1).strip()

        try:
            dados_json = json.loads(texto_gerado)
            yield json.dumps(dados_json) + "\n"
        except json.JSONDecodeError:
            yield json.dumps({"erro": f"O modelo não devolveu um JSON válido para {distrito}."}) + "\n"

