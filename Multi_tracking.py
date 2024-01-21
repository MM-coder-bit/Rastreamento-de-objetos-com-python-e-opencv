# -------------------------------------------------------------------------------------------------------------------------------#
# Rastreamento de Múltiplos Objetos com OpenCV

# Este código demonstra como usar o OpenCV para realizar o rastreamento de múltiplos objetos em uma sequência de vídeo.
# O código utiliza a função `cv2.legacy.MultiTracker_create()` para criar um objeto multitracker,
# que pode ser usado para rastrear vários objetos em um vídeo.
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Importar as bibliotecas necessárias
import cv2
import sys
from random import randint
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Definir os tipos de rastreadores

# O código define uma lista de tipos de rastreadores que podem ser usados pelo objeto multitracker. Esses tipos incluem:
# `BOOSTING`
# `MIL`
# `KCF`
# `TLD`
# `MEDIANFLOW`
# `MOSSE`
# `CSRT`
tracker_types = ['BOOSTING','MIL','KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Criar uma função para criar um rastreador pelo nome

# A função `createTrackerByName()` recebe um tipo de rastreador como argumento
# e retorna um objeto rastreador desse tipo. Se o tipo de rastreador não for reconhecido,
# a função retorna `None`.
def createTrackerByName(trackerType):
    if trackerType == tracker_types[0]:
        tracker = cv2.legacy.TrackerBoosting_create()
    elif trackerType == tracker_types[1]:
        tracker = cv2.legacy.TrackerMIL_create()
    elif trackerType == tracker_types[2]:
        tracker = cv2.legacy.TrackerKCF_create()
    elif trackerType == tracker_types[3]:
        tracker = cv2.legacy.TrackerTLD_create()
    elif trackerType == tracker_types[4]:
        tracker = cv2.legacy.TrackerMedianFlow_create()
    elif trackerType == tracker_types[5]:
        tracker = cv2.legacy.TrackerMOSSE_create()
    elif trackerType == tracker_types[6]:
        tracker = cv2.legacy.TrackerCSRT_create()
    else:
        tracker = None
        print('Nome incorreto')
        print('Os rastreadores disponíveis são: ')
        for t in tracker_types:
            print(t)

    return tracker
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Criar um objeto de captura de vídeo

# O código cria um objeto de captura de vídeo usando a função `cv2.VideoCapture()`.
# O objeto de captura de vídeo é usado para ler frames de um arquivo de vídeo.
cap = cv2.VideoCapture("videos/race.mp4")
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Ler o primeiro frame do vídeo

# O código lê o primeiro frame do vídeo usando o método `read()` do objeto de captura de vídeo.
# Se o frame não for lido com sucesso, o código imprime uma mensagem de erro e sai.
ok, frame = cap.read()
if not ok:
    print('Não é possível ler o arquivo de vídeo')
    sys.exit(1)

bboxes = []
colors = []
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Selecionar caixas delimitadoras para os objetos a serem rastreados

# O código usa a função `cv2.selectROI()` para permitir que o usuário selecione caixas delimitadoras para os objetos a serem rastreados.
# As caixas delimitadoras são armazenadas em uma lista chamada `bboxes`.
while True:
    bbox = cv2.selectROI('MultiTracker', frame, True)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0,255), randint(0,255))) # Gerar cores aleatórias para as caixas delimitadoras
    print('Pressione Q para sair das caixas de seleção e começar a rastrear')
    print('Pressione qualquer outra tecla para selecionar o próximo objeto')
    k = cv2.waitKey(0) & 0XFF
    if (k == 113):
        break

print('Caixas delimitadoras selecionadas {}'.format(bboxes))
print('Cores {}'.format(colors))
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Criar um objeto multitracker

# O código cria um objeto multitracker usando a função `cv2.legacy.MultiTracker_create()`.
# O objeto multitracker é usado para rastrear vários objetos em um vídeo.
trackertype = 'CSRT'
multiTracker = cv2.legacy.MultiTracker_create()
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Adicionar as caixas delimitadoras ao objeto multitracker

# O código adiciona as caixas delimitadoras ao objeto multitracker usando o método `add()` do objeto multitracker.
for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackertype), frame, bbox)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Atualizar o multitracker com o frame atual para obter as caixas delimitadoras dos objetos rastreados.
# A função `multiRastreador.update(frame)` retorna um valor booleano 'ok' indicando o sucesso da atualização,
# e 'boxes' contém as caixas delimitadoras atualizadas para cada objeto rastreado no frame atual.
    ok, boxes = multiTracker.update(frame)
# -------------------------------------------------------------------------------------------------------------------------------#

# -------------------------------------------------------------------------------------------------------------------------------#
# Iterar sobre a lista enumerada de caixas delimitadoras obtidas da atualização do multitracker.
# Converter os valores de ponto flutuante em 'newbox' para inteiros e extrair as coordenadas (x, y, w, h).
# Desenhar retângulos ao redor dos objetos rastreados no frame atual usando a função `cv2.rectangle` do OpenCV.
# Os retângulos são coloridos com base na lista 'colors', e os parâmetros especificam a espessura (2)
    for i, newbox in enumerate(boxes):
        (x, y, w, h) = [int(v) for v in newbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), colors[i], 2, 1)

    cv2.imshow('MultiTracker', frame)

    if cv2.waitKey(1) & 0XFF == 27:
        break
# -------------------------------------------------------------------------------------------------------------------------------#
