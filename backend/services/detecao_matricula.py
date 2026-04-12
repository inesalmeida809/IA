from ultralytics import YOLO
import cv2
import re

model = YOLO("license_plate_detector.pt")


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
                h, w, _ = img.shape

                pad_x = int((x2 - x1) * 0.05)
                pad_y = int((y2 - y1) * 0.1)

                x1 = max(0, x1 - pad_x)
                y1 = max(0, y1 - pad_y)
                x2 = min(w, x2 + pad_x)
                y2 = min(h, y2 + pad_y)

                crop = img[y1:y2, x1:x2]

                
                crop = cv2.resize(
                    crop, None, fx=3, fy=3,
                    interpolation=cv2.INTER_CUBIC
                )

               
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

           
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
                gray = clahe.apply(gray)

               
                _, thresh = cv2.threshold(
                    gray, 0, 255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )

                crop = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

                melhor_crop = crop

    if melhor_crop is not None:
        cv2.imwrite("debug_plate.jpg", melhor_crop)

    return melhor_crop


def validar_matricula(texto):
    padroes = [
        r"[A-Z]{2}[0-9]{2}[A-Z]{2}",
        r"[0-9]{2}[A-Z]{2}[0-9]{2}",
        r"[A-Z]{2}[0-9]{4}",
        r"[0-9]{4}[A-Z]{2}",
        r"[A-Z]{4}[0-9]{2}",
        r"[0-9]{2}[A-Z]{4}"
    ]

    for p in padroes:
        if re.fullmatch(p, texto):
            return True

    return False