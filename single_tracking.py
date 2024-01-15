# ------------------- instalação de pacotes ------------------- #
# pip install opencv-python==4.9.0
# pip install opencv-contrib-python==4.9.0
# ------------------------------------------------------------- #

# importar pacotes #
import cv2
import sys
from random import randint

# Versão Opencv #
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

# Tipos de rastreamentos #
tracker_types = ['BOOSTING', 
                 'MIL',
                 'KCF',
                 'TLD',
                 'MEDIANFLOW',
                 'MOSSE', 
                 'CSRT']

tracker_type = tracker_types[1]

# Selecionador do tipo de rastreamento #
if int(minor_ver) < 3 :
    tracker = tracker_type
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.legacy.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.legacy.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.legacy.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.legacy.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.legacy.TrackerMedianFlow_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.legacy.TrackerMOSSE_create()
    if tracker_type == 'CSRT':
        tracker = cv2.legacy.TrackerCSRT_create()

# Carregar o video #
video = cv2.VideoCapture('Videos/race.mp4')
# Verificar se o video esta disponivel #
if not video.isOpened():
    print('Não foi possivel encontrar o vídeo')
    sys.exit()

# Ler os frames dos videos #
ok, frame = video.read()
# Verifica se o vídeo não está corrompido #
if not ok:
    print('Não foi possivel ler o arquivo do video')
    sys.exit()

# Seleciona a região de interesse
bbox = cv2.selectROI(frame, False)
#print(bbox)

#Inicializa o tracker
ok = tracker.init(frame, bbox)
#print(ok)

# Random de cores para o bbox
colors = (randint(0,255), randint(0, 255), randint(0, 255))
#print(colors)