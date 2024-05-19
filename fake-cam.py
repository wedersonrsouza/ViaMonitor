import logging
import queue
import random
import sys
import threading
import time

import cv2
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')

# Variável compartilhada entre threads
currentFrame = None

def FakeCamera(Q, filename):
    """Leitura do arquivo de vídeo em sua taxa natural, armazenando o frame em uma variável global chamada 'currentFrame'."""
    logging.debug(f'[FakeCamera] Gerando stream de vídeo de {filename}')

    # Abrir vídeo
    video = cv2.VideoCapture(filename)
    if (video.isOpened() == False):
        logging.critical(f'[FakeCamera] Não foi possível abrir o vídeo {filename}')
        Q.put('ERROR')
        return

    # Obter altura, largura e quadros por segundo para saber quantas vezes ler um frame
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = video.get(cv2.CAP_PROP_FPS)
    logging.debug(f'[FakeCamera] h={h}, w={w}, fps={fps}')

    # Inicializar currentFrame
    global currentFrame
    currentFrame = np.zeros((h, w, 3), dtype=np.uint8)

    # Sinalizar ao main que estamos prontos
    Q.put('OK')

    while True:
        ret, frame = video.read()
        if ret == False:
            break
        # Armazenar o frame do vídeo onde o main pode acessá-lo
        currentFrame[:] = frame[:]
        # Tentar ler à taxa apropriada
        time.sleep(1.0 / fps)

    logging.debug('[FakeCamera] Finalizando')
    Q.put('DONE')

if __name__ == '__main__':
    # Criar uma fila para sincronizar e comunicar com nossa câmera falsa
    Q = queue.Queue()

    # Criar uma thread de câmera falsa que lê o vídeo em "tempo real"
    fc = threading.Thread(target=FakeCamera, args=(Q, 'videos/32864-394513950.mp4'))  # Substitua 'video.mov' pelo nome do seu arquivo de vídeo
    fc.start()

    # Aguardar a inicialização da câmera falsa
    logging.debug(f'[main] Aguardando a câmera acender e inicializar')
    msg = Q.get()
    if msg!= 'OK':
        sys.exit()
        
    while True:
        # Loop de processamento principal deve estar aqui - vamos apenas pegar alguns frames em diferentes momentos
        
        time_random = random.randint(1000, 8000)
                
        cv2.imshow('Video', currentFrame)
        res = cv2.waitKey(time_random)
        
        time.sleep(10)

        

    # Aguardar a finalização
    fc.join()
