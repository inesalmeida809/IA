from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("license_plate_detector.pt")


def preprocessar_para_ocr(crop):

    crop = cv2.resize(crop, None, fx=4.0, fy=4.0, interpolation=cv2.INTER_LANCZOS4)

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(denoised)

    adaptive = cv2.adaptiveThreshold(
        clahe_img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 5
    )

    _, otsu = cv2.threshold(clahe_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    otsu = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, morph_kernel)

  
    return [
        cv2.cvtColor(clahe_img, cv2.COLOR_GRAY2BGR),    
        cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR),     
        cv2.cvtColor(otsu, cv2.COLOR_GRAY2BGR),          
    ]


def detectar_matricula(caminho_img):
    img = cv2.imread(caminho_img)
    if img is None:
        return None

    results = model(img, conf=0.3)

    melhor_crop = None
    melhor_conf = 0

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])

            if conf > melhor_conf:
                melhor_conf = conf

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                h, w = img.shape[:2]

                
                pad_x = int((x2 - x1) * 0.05)
                pad_y = int((y2 - y1) * 0.1)

                x1 = max(0, x1 - pad_x)
                y1 = max(0, y1 - pad_y)
                x2 = min(w, x2 + pad_x)
                y2 = min(h, y2 + pad_y)

                melhor_crop = img[y1:y2, x1:x2].copy()

    if melhor_crop is not None:
        cv2.imwrite("debug_plate_raw.jpg", melhor_crop)

    return melhor_crop  