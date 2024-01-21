# -------------------------------------------------------------------------------------------------------------------------------#
# Rastreamento de Objeto com OpenCV

# Este código demonstra como usar o OpenCV para realizar o rastreamento de objeto em uma sequência de vídeo.
# O código utiliza a função `tracker.init()` para criar um objeto tracker,
# que pode ser usado para rastrear o objeto em um vídeo.
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Importar as bibliotecas necessárias
import cv2
import sys
from random import randint

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
#print(major_ver, minor_ver, subminor_ver)

# Definir os tipos de rastreadores

# O código define uma lista de tipos de rastreadores que podem ser usados pelo objeto multitracker. Esses tipos incluem:
# `BOOSTING`
# `MIL`
# `KCF`
# `TLD`
# `MEDIANFLOW`
# `MOSSE`
# `CSRT`
tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
tracker_type = tracker_types[6]

# -------------------------------------------------------------------------------------------------------------------------------#
# Condição para criar o rastreador
if int(minor_ver) < 3:
    tracker = tracker_type
else:
   if tracker_type == 'BOOSTING':
       tracker = cv2.legacy.TrackerBoosting_create()
   if tracker_type == 'MIL':
       tracker = cv2.TrackerMIL_create()
   if tracker_type == 'KCF':
       tracker = cv2.TrackerKCF_create()
   if tracker_type == 'TLD':
       tracker = cv2.legacy.TrackerTLD_create()
   if tracker_type == 'MEDIANFLOW':
       tracker = cv2.legacy.TrackerMedianFlow_create()
   if tracker_type == 'MOSSE':
       tracker = cv2.legacy.TrackerMOSSE_create()
   if tracker_type == 'CSRT':
       tracker = cv2.TrackerCSRT_create()

# -------------------------------------------------------------------------------------------------------------------------------#
# Criar um objeto de captura de vídeo

# O código cria um objeto de captura de vídeo usando a função `cv2.VideoCapture()`.
# O objeto de captura de vídeo é usado para ler frames de um arquivo de vídeo.
video = cv2.VideoCapture('videos/race.mp4')
if not video.isOpened():
    print('Não foi possível carregar o vídeo')
    sys.exit()

# Ler o primeiro frame do vídeo

# O código lê o primeiro frame do vídeo usando o método `read()` do objeto de captura de vídeo.
# Se o frame não for lido com sucesso, o código imprime uma mensagem de erro e sai.
ok, frame = video.read()
if not ok:
    print('Não foi possível ler o arquivo de vídeo')
    sys.exit()

# -------------------------------------------------------------------------------------------------------------------------------#
# Selecionar caixa delimitadora para o objeto a ser rastreado

# O código usa a função `cv2.selectROI()` para permitir que o usuário selecione caixa delimitadora para o objeto a ser rastreado.
# A caixa delimitadora é armazenada em uma variável chamada `bboxes`.
bbox = cv2.selectROI(frame, False)

# Inicializar o rastreador de objetos
ok = tracker.init(frame, bbox)

colors = (randint(0, 255), randint(0, 255), randint(0, 255)) # Gerar cores aleatórias para as caixas delimitadoras

# Detecta o objeto em todo o vídeo

# Enquanto rastreia o objeto a cada frame, é apresentado dados de 'fps' e
# posição da caixa delimitadora na tela.
while True:
    ok, frame = video.read()
    if not ok:
        break

    # https://docs.opencv.org/master/dc/d71/tutorial_py_optimization.html
    timer = cv2.getTickCount()
    ok, bbox = tracker.update(frame)
    
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), colors, 2, 1)
    else:
        cv2.putText(frame, 'Falha no rastreamento', (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)

    cv2.putText(frame, tracker_type + ' Tracker', (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, .75, (50, 170, 50), 2)

    cv2.putText(frame, 'FPS: ' + str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, .75, (50, 170, 50), 2)

    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0XFF == 27:
        break