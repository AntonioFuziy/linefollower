from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import L298

camera = PiCamera
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    #Aqui se encaixaria o código de visão computacional para o movimento do robô também ser realizado

    frame = image

    # Crop the image
    #======================================================================================================
    # ISSO PRECISA SER ALTERADO NO MOMENTO DE TESTE COM A RASP
    crop_img = frame[600:940, 500:800]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
    ret,thresh = cv2.threshold(blur,230,255,cv2.THRESH_BINARY)

    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        try:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

            if cx >= 120:
                #print("Turn Left!")
                L298.left(delay)

            if cx < 120 and cx > 50:
                #print("On Track!")
                L298.forward(delay)

            if cx <= 50:
                #print("Turn Right")
                L298.right(delay)
        except:
            pass

    else:
        print("Dont see the line")

    #Display the resulting frame

    cv2.imshow('frame',crop_img)
    # cv2.imshow("gray", gray)
    # cv2.imshow("blur", blur)
    # cv2.imshow("thresh", thresh)

    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break