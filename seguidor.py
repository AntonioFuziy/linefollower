# -*- coding:utf-8 -*-

#Essa primeira linha é necessária por conta de um erro com o python 2
import cv2
import numpy as np
import time
import math

#path do video
#OBS: coloque um video do seu computador na sua file porque videos são pesados para dar upload no github
#video = "video.mp4"

#path da imagem
imagem = "imagem.jpg"

#capturando o video de exemplo
#cap = cv2.VideoCapture(video)

#acessando webcam
cap = cv2.VideoCapture(0)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#lendo uma foto de exemplo
image = cv2.imread(imagem)
image = cv2.resize(image, (512, 288))

#================================================================
#sempre se utiliza "while True:" quando se trabalha com video, webcam ou outras reproduções de imagens que mudem de frames, pois
#esses frames vão estar sempre mudando de acordo com a reprodução do vídeo, então é necessário um loop para realizar a visão computacional
#de cada frame do que está sendo reproduzido.

while True:
    #lendo a captura da camera como segundo argumento (frame)
    #frame representa o video em bgr
    ret, webcam = cap.read()

#================================================================
    #Conversões de cores

    #OBS: Aqui só foi convertido o vídeo, mas o código para conversão tanto dos vídeos como da webcam e de fotos, é o mesmo
    #Por exemplo: webcam_rgb = cv2.cvtColor(webcam, cv2.COLOR_BGR2RGB) | e para a foto image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #convertendo de bgr para rgb
    #sempre terá essa estrutura -> a imagem/video de saída recebe a imagem/video de entrada (frame no caso) e converte de BGR TO RGB ou outras conversões a serem relizadas
    rgb = cv2.cvtColor(webcam, cv2.COLOR_BGR2RGB)
    #convertendo de bgr para gray
    gray = cv2.cvtColor(webcam, cv2.COLOR_BGR2GRAY)
    #convertendo de bgr para hsv
    hsv = cv2.cvtColor(webcam, cv2.COLOR_BGR2HSV)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #convertendo de bgr para gray
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #convertendo de bgr para hsv
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#================================================================
    #mostrando uma janela com o vídeo e a webcam
    #OBS: o primeiro argumento é só o nome que você dá a janela e o próximo é o que você quer que a janela mostre, no caso o vídeo ou 
    #webcam ou foto
    cv2.imshow("webcam", webcam)
    cv2.imshow("image", image)
    #cv2.imshow("video",video)

    #caso queira reproduzir na janela o video ou webcam com as cores convertidas, descomente as linhas abaixo
    #cv2.imshow("rgb", rgb)
    #cv2.imshow("gray", gray)
    #cv2.imshow("hsv", hsv)

    #cv2.imshow("image_rgb", image_rgb)
    #cv2.imshow("image_gray", image_gray)
    #cv2.imshow("image_hsv", image_hsv)



#================================================================
    #essas linhas do final são necessárias para que o código não entre em loop infinito e trave seu programa.

    #esse if indica que quando você está na janela de reprodução dos vídeos e aperta a tecla "q", o programa para de rodar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#parando de rodar o programa
cap.release()
cv2.destroyAllWindows()