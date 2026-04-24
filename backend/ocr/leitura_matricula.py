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
        return []

    janelas = [texto_limpo[i:i + 6] for i in range(0, len(texto_limpo) - 5)]
    candidatos = []

    for janela in janelas:
        for padrao_tipo in PADROES_TIPO:
            corrigido, pontos_padrao = corrigir_confusoes_ocr(janela, padrao_tipo)
            if not corrigido:
                continue

            candidatos.append({
                "texto": corrigido,
                "pontos_padrao": pontos_padrao,
                "valido": validar_matricula(corrigido),
            })

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
            continue

        resultados_ordenados = sorted(
            resultados,
            key=lambda r: min([p[0] for p in r[0]])
        )

        texto_completo = "".join([r[1] for r in resultados_ordenados])
        confianca_media = sum([r[2] for r in resultados]) / len(resultados)

        texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_completo.upper())
        candidatos_locais = gerar_candidatos(texto_limpo)

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
        return None

    validos = [c for c in candidatos if c["valido"]]
    if validos:
        return max(validos, key=lambda x: (x["pontos_padrao"], x["confianca"]))["texto"]

    return max(candidatos, key=lambda x: (x["pontos_padrao"], x["confianca"]))["texto"]


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
        return {"erro": "MATRICULA_NAO_ENCONTRADA"}
    
    variantes = preprocessar_para_ocr(plate_raw)

    texto = tentar_ocr_em_variantes(variantes)

    if not texto:
        return {"erro": "OCR_SEM_RESULTADO"}

  
    matricula = formatar_matricula(texto)

    if matricula is None:
        return {"erro": f"TEXTO_INCOMPLETO: {texto}"}

    valida = validar_matricula(texto)

    return {
        "matricula": matricula,
        "valida": valida,
        "texto_bruto": texto
    }