import pytesseract
import cv2
import shutil
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ler_matricula(file):
    caminho = "temp.jpg"
    
    with open (caminho, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    img = cv2.imread(caminho)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    texto = pytesseract.image_to_string(thresh)
    
    texto = texto.upper()
    texto = re.sub(r'[^A-Z0-9-]', '', texto)

    return texto