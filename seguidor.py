import cv2
import numpy as np
import time
import math

video = "video.mp4"

cap = cv2.VideoCapture(video)

# mask exemplo para linha

#lower_white = np.array([0, 0, 212])
#upper_white = np.array([131, 255, 255])
# Threshold the HSV image
#mask = cv2.inRange(hsv, lower_white, upper_white)


coef_angular_positivo = []
coef_angular_negativo = []
coef_linear_positivo = []
coef_linear_negativo = []


while True:
    ret, frame = cap.read()

    lista_xi = []
    lista_yi = []

    x_ponto_fuga = []
    y_ponto_fuga = []

    avg_x=0
    avg_y=0

    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ret, threshold = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(threshold, 50, 150, apertureSize=3)
    edges2 = cv2.Canny(gray, 240, 255, apertureSize=3)

    low = np.array([220, 50, 50])
    high = np.array([255, 255, 255])

    mask = cv2.inRange(frame, low, high)

    edges3 = cv2.Canny(mask, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges3, 1, np.pi/180, 200)

    if lines is not None:
        for line in lines:
            for rho,theta in line:
                m = np.cos(theta)
                n = np.sin(theta)

                if 0.7 > m > 0.6:
                    coef_angular_positivo.append(m)
                    coef_linear_positivo.append(n)
                    x0 = m*rho
                    y0 = n*rho
                    x1 = int(x0 + 1000*(-n))
                    y1 = int(y0 + 1000*(m))
                    x2 = int(x0 - 1000*(-n))
                    y2 = int(y0 - 1000*(m))
                    line = cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)
                
                elif -0.7 > m > -0.8:
                    coef_angular_negativo.append(m)
                    coef_linear_negativo.append(n)
                    x0 = m*rho
                    y0 = n*rho
                    x3 = int(x0 + 1000*(-n))
                    y3 = int(y0 + 1000*(m))
                    x4 = int(x0 - 1000*(-n))
                    y4 = int(y0 - 1000*(m))
                    line = cv2.line(frame,(x3,y3),(x4,y4),(0,255,0),3)

                    try:
                        h1 = coef_linear_positivo[len(coef_linear_positivo)-1]
                        m1 = coef_angular_positivo[len(coef_angular_positivo)-1]

                        h2 = coef_linear_negativo[len(coef_linear_negativo)-1]
                        m2 = coef_angular_negativo[len(coef_angular_negativo)-1]
                        
                        xi = ((x1*y2 - y1*x2)*(x3 - x4) - (x1-x2)*(x3*y4 - y3*x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))#((h2-h1)/(m1-m2))
                        yi = ((x1*y2 - y1*x2)*(y3 - y4) - (y1-y2)*(x3*y4 - y3*x4))/((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))#(m1*xi) + h1

                        lista_xi.append(xi)
                        lista_yi.append(yi)

                        x_ponto_fuga.append(xi)
                        y_ponto_fuga.append(yi)
                    
                    except:
                        pass
                else:
                    pass
    try:
        avg_x = int(np.mean(x_ponto_fuga))
        avg_y = int(np.mean(y_ponto_fuga))
        cv2.circle(frame, (avg_x,avg_y), 3, (255,0,0), 5)
    except:
        pass
                
                # x0 = m*rho
                # y0 = n*rho
                # x1 = int(x0 + 1000*(-n))
                # y1 = int(y0 + 1000*(m))
                # x2 = int(x0 - 1000*(-n))
                # y2 = int(y0 - 1000*(m))
            
            #line = cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)

    cv2.imshow('imagem', frame)
    # cv2.imshow('threshold', threshold)
    cv2.imshow("egdes3", edges3)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()