import sqlite3
import threading
import time

import cv2
import numpy as np


# Função para conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('vehicle_passages.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vehicle_passages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        license_plate TEXT NOT NULL,
                        image BLOB NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    return conn, cursor

# Função para capturar e processar imagens da câmera
def capture_and_process_camera(conn, cursor):
    cap = cv2.VideoCapture('http://IP_DA_CAMERA')  # Substitua pelo IP da sua câmera
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Aplicar OpenALPR na imagem
        result = alpr.recognize_ndarray(frame)
        
        if len(result['results']) > 0:
            license_plate = result['results'][0]['plate']
            
            # Salvar a imagem no banco de dados
            _, buffer = cv2.imencode('.jpg', frame)
            cursor.execute("INSERT INTO vehicle_passages (license_plate, image) VALUES (?,?)", (license_plate, buffer))
            conn.commit()
        
        time.sleep(1)  # Intervalo entre capturas

if __name__ == "__main__":
    alpr = None
    try:
        alpr = openalpr.OpenALPR()
        alpr.setTopN(10)
        alpr.setDefaultMode(alpr.EASY_MODE)
        alpr.start()

        conn, cursor = connect_db()
        thread = threading.Thread(target=capture_and_process_camera, args=(conn, cursor))
        thread.daemon = True
        thread.start()

        input("Pressione Enter para parar...")
    except Exception as e:
        print(e)
    finally:
        if alpr:
            alpr.stop()
        conn.close()
