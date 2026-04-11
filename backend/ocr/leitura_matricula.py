import cv2
import re
import easyocr
from services.detecao_matricula import detectar_matricula, validar_matricula

reader = easyocr.Reader(['en'], gpu=False)


def corrigir_formato_pt(texto):
    texto = list(texto)
    for i, c in enumerate(texto):
        if i in [0, 1, 4, 5]:
            mapa = {'1': 'I', '0': 'O', '5': 'S', '8': 'B', '2': 'Z', '6': 'G'}
            texto[i] = mapa.get(c, c)
        elif i in [2, 3]:
            mapa = {'O': '0', 'D': '0', 'Q': '0', 'I': '1',
                    'L': '1', 'Z': '2', 'S': '5', 'B': '8'}
            texto[i] = mapa.get(c, c)
    return "".join(texto)


def formatar_matricula(texto):
    if len(texto) == 6:
        return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
    return texto


def ler_texto(img):
    try:
        result = reader.readtext(
            img,
            detail=0,
            allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
        print("RAW OCR:", result)
        return "".join(result)
    except Exception as e:
        print("ERRO OCR:", e)
        return ""


def limpar_texto(texto):
    texto = texto.upper()
    texto = re.sub(r'[^A-Z0-9]', '', texto)
    return texto[:6]


def ler_matricula(file):
    caminho = "temp.jpg"

    conteudo = file.file.read()
    with open(caminho, "wb") as buffer:
        buffer.write(conteudo)

    plate = detectar_matricula(caminho)

    if plate is None:
        return "MATRICULA_NAO_ENCONTRADA"

    print(f"Crop shape: {plate.shape}")
    cv2.imwrite("debug_plate_final.jpg", plate)

    texto = ler_texto(plate)
    texto = limpar_texto(texto)

    if not texto:
        return "SEM_TEXTO"

    texto = corrigir_formato_pt(texto)

    if not validar_matricula(texto):
        return f"FORMATO_INVALIDO:{texto}"

    return formatar_matricula(texto)