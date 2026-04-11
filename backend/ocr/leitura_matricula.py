import cv2
import re
import easyocr

from services.detecao_matricula import (
    detectar_matricula,
    validar_matricula
)

reader = easyocr.Reader(['en'], gpu=False)


def corrigir_formato_pt(texto):

    if re.fullmatch(r"[0-9]{4}[A-Z]{2}", texto):
        return texto

    texto = list(texto)

    for i, c in enumerate(texto):

    
        if i in [0, 1, 4, 5]:
            mapa = {
                '1': 'I', '0': 'O', '5': 'S',
                '8': 'B', '2': 'Z', '6': 'G',
                '4': 'A', 'J': 'I'
            }
            texto[i] = mapa.get(c, c)

      
        elif i in [2, 3]:
            mapa = {
                'O': '0', 'D': '0', 'Q': '0',
                'I': '1', 'L': '1', 'J': '1',
                'Z': '2', 'S': '5', 'B': '8'
            }
            texto[i] = mapa.get(c, c)

    return "".join(texto)


def formatar_matricula(texto):
    if len(texto) == 6:
        return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"
    return texto


def limpar_texto(texto):
    texto = texto.upper()
    texto = re.sub(r'[^A-Z0-9]', '', texto)
    return texto.strip()


def extrair_matricula_valida(texto):
    candidatos = re.findall(r'[A-Z0-9]{6}', texto)

    for c in candidatos:
        c_corrigido = corrigir_formato_pt(c)
        if validar_matricula(c_corrigido):
            return c_corrigido

    return ""


def escolher_melhor_resultado(resultados):
    for r in resultados:
        r_limpo = limpar_texto(r)
        r_corrigido = corrigir_formato_pt(r_limpo)

        if validar_matricula(r_corrigido):
            return r_corrigido

    return limpar_texto(resultados[0]) if resultados else ""


def ler_texto(img):
    try:
        resultados = []

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        variantes = [gray]

        # threshold
        _, th = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        variantes.append(th)

        # blur + threshold
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, th2 = cv2.threshold(
            blur, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        variantes.append(th2)

        for v in variantes:
            v = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)

            result = reader.readtext(
                v,
                detail=0,
                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            )

            texto = "".join(result)
            resultados.append(texto)

        print("OCR VARIANTES:", resultados)

        return resultados

    except Exception as e:
        print("ERRO OCR:", e)
        return []


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

  
    h, w, _ = plate.shape
    plate = plate[:, :int(w * 0.8)]

  
    plate = cv2.resize(plate, None, fx=4, fy=4,
                       interpolation=cv2.INTER_CUBIC)

    cv2.imwrite("debug_plate_cortada.jpg", plate)

    resultados = ler_texto(plate)

    if not resultados:
        return "SEM_TEXTO"

    texto = escolher_melhor_resultado(resultados)

    if not texto:
        return f"FORMATO_INVALIDO:{resultados}"

    return formatar_matricula(texto)