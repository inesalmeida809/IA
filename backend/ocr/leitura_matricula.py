import cv2
import re
import easyocr
from services.detecao_matricula_service import detectar_matricula, preprocessar_para_ocr

reader = easyocr.Reader(
    ['en'],
    gpu=False,
)

ALLOWLIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

PADROES = [
    r"[A-Z]{2}[0-9]{2}[A-Z]{2}",  
    r"[0-9]{2}[A-Z]{2}[0-9]{2}",  
    r"[A-Z]{2}[0-9]{4}",         
    r"[0-9]{4}[A-Z]{2}",          
]

PADROES_TIPO = [
    "LLDDLL",
    "DDLLDD",
    "LLDDDD",
    "DDDDLL",
]

LETRA_PARA_DIGITO = {
    'O': '0',
    'I': '1',
    'Z': '2',
    'S': '5',
    'B': '8',
    'G': '6',
}

DIGITO_PARA_LETRA = {
    '0': 'O',
    '1': 'I',
    '2': 'Z',
    '5': 'S',
    '8': 'B',
    '6': 'G',
}


def corrigir_confusoes_ocr(texto, padrao_tipo):
    """Ajusta caracteres ambíguos (O/0, I/1, ...) conforme o padrão esperado."""
    if len(texto) != 6:
        return None, -1

    convertido = []
    pontuacao = 0

    for i, char in enumerate(texto):
        esperado = padrao_tipo[i]

        if esperado == 'D':
            if char.isdigit():
                convertido.append(char)
                pontuacao += 2
            elif char in LETRA_PARA_DIGITO:
                convertido.append(LETRA_PARA_DIGITO[char])
                pontuacao += 1
            else:
                return None, -1
        else:
            if char.isalpha():
                convertido.append(char)
                pontuacao += 2
            elif char in DIGITO_PARA_LETRA:
                convertido.append(DIGITO_PARA_LETRA[char])
                pontuacao += 1
            else:
                return None, -1

    return ''.join(convertido), pontuacao


def gerar_candidatos(texto_limpo):
    if len(texto_limpo) < 6:
        print(f"[DEBUG] gerar_candidatos: texto muito curto '{texto_limpo}' ({len(texto_limpo)} chars)")
        return []

    janelas = [texto_limpo[i:i + 6] for i in range(len(texto_limpo) - 5)]
    candidatos = []

    for j, janela in enumerate(janelas):
        for padrao_tipo in PADROES_TIPO:
            corrigido, pontos_padrao = corrigir_confusoes_ocr(janela, padrao_tipo)
            if not corrigido:
                continue

            valido = validar_matricula(corrigido)
            candidatos.append({
                "texto": corrigido,
                "pontos_padrao": pontos_padrao,
                "valido": valido,
            })
            if valido:
                print(f"[DEBUG] Candidato VÁLIDO encontrado: {corrigido} (janela {j}: '{janela}', padrão: {padrao_tipo})")

    return candidatos


def validar_matricula(texto):
    for p in PADROES:
        if re.fullmatch(p, texto):
            return True
    return False


def tentar_ocr_em_variantes(variantes):
    """Corre OCR nas várias versões pré-processadas e escolhe o melhor resultado."""
    candidatos = []

    for i, img in enumerate(variantes):
        resultados = reader.readtext(
            img,
            allowlist=ALLOWLIST,
            detail=1,
            paragraph=False,
            rotation_info=None,
        )

        if not resultados:
            print(f"[DEBUG] Variante {i}: sem resultados OCR")
            continue

        resultados_ordenados = sorted(
            resultados,
            key=lambda r: min([p[0] for p in r[0]])
        )

        texto_completo = "".join([r[1] for r in resultados_ordenados])
        confianca_media = sum([r[2] for r in resultados]) / len(resultados)

        texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_completo.upper())
        print(f"[DEBUG] Variante {i}: texto_completo='{texto_completo}' -> texto_limpo='{texto_limpo}' (confiança: {confianca_media:.2f})")
        candidatos_locais = gerar_candidatos(texto_limpo)
        print(f"[DEBUG] Variante {i}: {len(candidatos_locais)} candidatos gerados")

        for c in candidatos_locais:
            candidatos.append({
                "texto": c["texto"],
                "confianca": confianca_media,
                "pontos_padrao": c["pontos_padrao"],
                "valido": c["valido"],
                "variante": i,
            })

        cv2.imwrite(f"debug_variante_{i}.jpg", img)

    if not candidatos:
        print("[DEBUG] tentar_ocr_em_variantes: nenhum candidato encontrado")
        return None

    validos = [c for c in candidatos if c["valido"]]
    if validos:
        melhor = max(validos, key=lambda x: (x["pontos_padrao"], x["confianca"]))
        print(f"[DEBUG] Matrícula válida selecionada: {melhor['texto']} (pontos: {melhor['pontos_padrao']}, confiança: {melhor['confianca']:.2f})")
        return melhor["texto"]

    melhor = max(candidatos, key=lambda x: (x["pontos_padrao"], x["confianca"]))
    print(f"[DEBUG] Nenhuma matrícula válida, selecionando melhor candidato: {melhor['texto']} (pontos: {melhor['pontos_padrao']}, confiança: {melhor['confianca']:.2f})")
    return melhor["texto"]


def formatar_matricula(texto):
    if len(texto) < 6:
        return None  
    return f"{texto[:2]}-{texto[2:4]}-{texto[4:6]}"


def ler_matricula(file):
    caminho = "temp.jpg"

    conteudo = file.file.read()
    with open(caminho, "wb") as buffer:
        buffer.write(conteudo)
    plate_raw = detectar_matricula(caminho)

    if plate_raw is None:
        print("[DEBUG] ler_matricula: matrícula não detectada pelo YOLO")
        return {"erro": "MATRICULA_NAO_ENCONTRADA"}
    
    print("[DEBUG] ler_matricula: matrícula detectada, iniciando OCR...")
    variantes = preprocessar_para_ocr(plate_raw)

    texto = tentar_ocr_em_variantes(variantes)

    if not texto:
        print("[DEBUG] ler_matricula: OCR sem resultado")
        return {"erro": "OCR_SEM_RESULTADO"}

    matricula = formatar_matricula(texto)

    if matricula is None:
        print(f"[DEBUG] ler_matricula: texto incompleto '{texto}'")
        return {"erro": f"TEXTO_INCOMPLETO: {texto}"}

    valida = validar_matricula(texto)
    print(f"[DEBUG] ler_matricula: resultado final '{matricula}' (valida: {valida})")

    return {
        "matricula": matricula,
        "valida": valida,
        "texto_bruto": texto
    }