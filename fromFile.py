import cv2
import numpy as np
import openalpr

# Inicializar OpenALPR
alpr = openalpr.Alpr(country='br', )
alpr.setTopN(10)
alpr.setDefaultMode(openalpr.EASY_MODE)
alpr.start()

# Carregar o vídeo para simulação
cap = cv2.VideoCapture('videos/32864-394513950.mp4')

while True:
    # Ler um frame do vídeo
    ret, frame = cap.read()
    if not ret:
        break

    # Convertendo o frame para escala de cinza (opcional, depende do seu caso de uso)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Processar o frame com OpenALPR
    result = alpr.recognize_ndarray(gray)

    # Verificar se alguma placa foi reconhecida
    if len(result['results']) > 0:
        for plate in result['results']:
            print("Placa reconhecida:", plate['plate'])

    # Mostrar o frame original (para visualização)
    cv2.imshow('Fake Camera', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
