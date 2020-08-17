# -*- coding:utf-8 -*-
import cv2
import numpy as np

video = "assets/linha.webm"
video_capture = cv2.VideoCapture(video)

while True:
    ret, frame = video_capture.read()

    #======================================================================================================
    # ISSO PRECISA SER ALTERADO NO MOMENTO DE TESTE COM A RASP
    crop_img = frame[630:1000, 500:770]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    ret, thresh = cv2.threshold(blur, 230,255, cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    print("Number of contourns detected {}".format(len(contours)))

    #pegando o primeiro contorno identificado, a linha abaixo pega todos os contornos identificados na imagem
    cv2.drawContours(crop_img, contours, 0, (0,255,0), 3)
    # cv2.drawContours(crop_img, contours, -1, (0,255,0), 3)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        try:
            #encontrando o centro do maior contorno
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            #traçando o centro do contorno no vídeo
            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

            if cx >= 120:
                print("Turn Left!")

            if cx < 120 and cx > 50:
                print("On Track!")

            if cx <= 50:
                print("Turn Right")
        except:
            pass

    else:
        print("Dont see the line")

    #cv2.imshow("frame", thresh)
    cv2.imshow("crop_img", crop_img)
    # cv2.imshow("thresh", thresh)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break