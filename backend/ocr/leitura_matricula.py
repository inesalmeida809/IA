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


def corrigir_confusoes_ocr(texto):
    """Corrige confusões comuns do OCR em contexto de matrícula."""
    correcoes = {
        'O': '0',  
        'I': '1',
        'Z': '2',
        'S': '5',
        'B': '8',
        'G': '6',
    }

  
    resultado = list(texto[:6].ljust(6))
    for i, c in enumerate(resultado):
        if i in (2, 3):  
            if c in correcoes:
                resultado[i] = correcoes[c]
        elif i in (0, 1, 4, 5):  
            if c.isdigit():
                inv = {'0': 'O', '1': 'I', '2': 'Z', '5': 'S', '8': 'B', '6': 'G'}
                resultado[i] = inv.get(c, c)
    return ''.join(resultado)


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

        texto_completo = "".join([r[1] for r in resultados])
        confianca_media = sum([r[2] for r in resultados]) / len(resultados)

        texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_completo.upper())
        texto_corrigido = corrigir_confusoes_ocr(texto_limpo)

        candidatos.append({
            "texto": texto_corrigido,
            "confianca": confianca_media,
            "valido": validar_matricula(texto_corrigido),
            "variante": i
        })

        cv2.imwrite(f"debug_variante_{i}.jpg", img)

    if not candidatos:
        return None

    validos = [c for c in candidatos if c["valido"]]
    if validos:
        return max(validos, key=lambda x: x["confianca"])["texto"]

    return max(candidatos, key=lambda x: x["confianca"])["texto"]


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