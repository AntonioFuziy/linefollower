import RPi.GPIO as GPIO
import numpy as np
import cv2
from time import sleep

in1 = 26 
in2 = 20 
in3 = 13
in4 = 12
en1 = 21 
en2 = 16
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p=GPIO.PWM(en1,1000)
p2=GPIO.PWM(en2,1000)

p.start(25)
p2.start(25)

video = "assets/line.mp4"
video_capture = cv2.VideoCapture(video)

delay = 1

while(True):
    # Capture the frames
    ret, frame = video_capture.read()

    if ret == False:
        print("The video has ended!")
        break

    # Crop the image -> original: ([600:940, 500:800])
    #======================================================================================================
    # ISSO PRECISA SER ALTERADO NO MOMENTO DE TESTE COM A RASP
    # crop_img = frame[600:940, 500:840]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
    ret,thresh = cv2.threshold(blur,130,255,cv2.THRESH_BINARY_INV)

    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    i=0
    for c in contours:
        i+=1

        # c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        try:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
            cv2.circle(frame, (cx, cy), 10, (255, 0, 0), 2)
            cv2.drawContours(frame, [c], -1, (0,255,0), 1)

            # 340 = tamanho da tela em x
            # 340-(340/3)-20
            if cx >= 207:
                print("Turn Right!")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p.ChangeDutyCycle(50)
                p2.ChangeDutyCycle(25)
                
            # 340 = tamanho da tela em y
            # (340/3)-20
            elif cx <= 133:
                print("Turn Left!")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p.ChangeDutyCycle(25)
                p2.ChangeDutyCycle(50)

            else:
                print("On Track")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p.ChangeDutyCycle(50)
                p2.ChangeDutyCycle(50)
        except:
            pass

    else:
        print("Dont see the line")

    #Display the resulting frame
    cv2.imshow('frame', frame)
    # cv2.imshow("gray", gray)
    # cv2.imshow("blur", blur)
    # cv2.imshow("thresh", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
GPIO.cleanup()
video_capture.release()
cv2.destroyAllWindows()






