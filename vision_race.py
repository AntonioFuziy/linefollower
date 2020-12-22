import numpy as np
import cv2

video = "assets/line.mp4"
video_capture = cv2.VideoCapture(video)

while True:
    ret, frame = video_capture.read()

    if ret == False:
        print("The video has ended!")
        break

    crop_img = frame[600:940, 500:840]

    blur = cv2.GaussianBlur(crop_img,(5,5),0)

    ret,thresh = cv2.threshold(blur,230,255,cv2.THRESH_BINARY)

    cv2.imshow("thresh", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
