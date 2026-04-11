from services.detecao_matricula import detectar_matricula

import cv2
import re
import easyocr

reader = easyocr.Reader(['en'])

def corrigir_e_formatar_matricula(texto):
    texto = re.sub(r'[^A-Z0-9]', '', texto)

    if len(texto) < 6:
        return texto

    texto = texto[:6]

    resultado = []

    for i, c in enumerate(texto):

        if i in [0, 1, 4, 5]:
            if c.isdigit():
                mapa = {
                    "0": "O",
                    "1": "I",
                    "2": "Z",
                    "5": "S",
                    "8": "B",
                    "6": "G",
                    "7": "T" 
                }
                c = mapa.get(c, c)

 
        elif i in [2, 3]:
            if c.isalpha():
                mapa = {
                    "O": "0",
                    "I": "1",
                    "Z": "2",
                    "S": "5",
                    "B": "8",
                    "G": "6",
                    "T": "7",
                    "F": "7", 
                    "A": "4"
                }
                c = mapa.get(c, c)

        resultado.append(c)

    texto_corrigido = "".join(resultado)

    return f"{texto_corrigido[:2]}-{texto_corrigido[2:4]}-{texto_corrigido[4:]}"

def ler_matricula(file):
    caminho = "temp.jpg"

   
    conteudo = file.file.read()
    with open(caminho, "wb") as buffer:
        buffer.write(conteudo)

  
    plate = detectar_matricula(caminho)
    
    if plate is None:
        return "MATRICULA_NAO_ENCONTRADA"

    plate = cv2.resize(plate, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    h, w, _ = plate.shape
    plate = plate[:, int(w * 0.2):]

    resultados = reader.readtext(plate)

    if resultados:
    
        texto = max(resultados, key=lambda x: len(x[1]))[1]
    else:
        texto = ""

 
    texto = texto.upper()
    texto = re.sub(r'[^A-Z0-9]', '', texto)

    texto = corrigir_e_formatar_matricula(texto)

    return texto