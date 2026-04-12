from services.detecao_matricula_service import detectar_matricula

import cv2
import re
import easyocr

reader = easyocr.Reader(['en'])


def formatar_matricula(texto):
    texto = re.sub(r'[^A-Z0-9]', '', texto)


    texto = texto.ljust(6, "_")

    texto = texto[:6]

    return f"{texto[:2]}-{texto[2:4]}-{texto[4:]}"


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
     
        texto = max(resultados, key=lambda x: x[2])[1]
    else:
        texto = ""

  
    texto = texto.upper()
    texto = re.sub(r'[^A-Z0-9]', '', texto)

    texto = formatar_matricula(texto)

    return texto