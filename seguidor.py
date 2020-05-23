import cv2
import numpy as np
import time
import math

video = "video.mp4"

cap = cv2.VideoCapture(video)

while True:
    ret, frame = cap.read()

    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, threshold = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(threshold, 50, 150, apertureSize=3)
    edges2 = cv2.Canny(gray, 230, 255, apertureSize=3)

    cv2.imshow("Canny", edges2)


    lines = cv2.HoughLines(edges2, 1, np.pi/180, 200)

    #m < -1.6 and m > 2

    for rho, theta in lines[0]:
        m = np.cos(theta)
        n = np.sin(theta)
        
        x0 = m*rho
        y0 = n*rho
        x1 = int(x0 + 1000*(-n))
        y1 = int(y0 + 1000*(m))
        x2 = int(x0 - 1000*(-n))
        y2 = int(y0 - 1000*(m))
    
    line = cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)

    cv2.imshow('imagem', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()