#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = ["Rachel P. B. Moraes", "Fabio Miranda"]

import rospy
import numpy as np
from numpy import linalg
from tf import transformations
from tf import TransformerROS
import tf2_ros
import cv2
import math
from geometry_msgs.msg import Twist, Vector3, Pose, Vector3Stamped
from ar_track_alvar_msgs.msg import AlvarMarker, AlvarMarkers
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import Header
from sensor_msgs.msg import LaserScan
from cv_bridge import CvBridge, CvBridgeError
import rospkg

import identificador_pista
import cormodule
import time


bridge = CvBridge() #arquivo ros pra abrir o cv_img
cv_image = None # Cv Image
rospack = rospkg.RosPack() 

# Def center_mass
media_pista = []
centro_pista = []

# Atrasos e delays - Descarta imagens que chegam atrasadas demais
# Só usar se os relógios ROS da Raspberry e do Linux desktop estiverem sincronizados.  
atraso = 1.5E9 # 1 segundo e meio. Em nanossegundos
check_delay = False

# Conversão do sistema de coordenadas
tfl = 0
tf_buffer = tf2_ros.Buffer()

# Inicializando velocidades - por default gira no sentido anti-horário
w = 0.5
v = 0.25
vel_direita = Twist(Vector3(v,0,0), Vector3(0,0,-w))
vel_esquerda = Twist(Vector3(v,0,0), Vector3(0,0,w))
vel_frente = Twist(Vector3(v,0,0), Vector3(0,0,0))
vel_parado = Twist(Vector3(0,0,0), Vector3(0,0,0))


# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
    global cv_image
    global media_pista
    global centro_pista
    global resultados
    global identifica_contorno_pista


    # Para robô real
    now = rospy.get_rostime()
    imgtime = imagem.header.stamp
    lag = now-imgtime # calcula o lag
    delay = lag.nsecs

    if delay > atraso and check_delay==True:
        print("Descartando por causa do delay do frame:", delay)
        return 
    try:
        antes = time.clock()
        temp_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        aruco_image = temp_image.copy()

        depois = time.clock()
        # Desnecessário - Hough e MobileNet já abrem janelas

        # cv_image = cv2.flip(cv_image, -1) # Descomente se for robo real
        media_pista, centro_pista =  identificador_pista.identifica_pista(aruco_image)
        
        # cv2.imshow("cv_image", temp_image)
        cv2.imshow("aruco_image", aruco_image)
        cv2.waitKey(1)

    except CvBridgeError as e:
        print('ex', e)
    path = rospack.get_path('Projeto-Robocom')


if __name__=="__main__":
    rospy.init_node("seguidor") 

    topico_imagem = "/camera/image/compressed"
    # topico_imagem = "/raspicam/image_raw/compressed" # Use para robo real
    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)
    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    tfl = tf2_ros.TransformListener(tf_buffer) #conversao do sistema de coordenadas 

    margem = 80
    try:
        while not rospy.is_shutdown():
            try:
                if media_pista[0] > (centro_pista[0] + margem):
                    velocidade_saida.publish(vel_direita)
                    print("Direita")
                elif media_pista[0] < (centro_pista[0] - margem):
                    velocidade_saida.publish(vel_esquerda)
                    print("Esquerda")
                else:
                    velocidade_saida.publish(vel_frente)
                    print("Frente")
                
                rospy.sleep(0.1)


            except:
                pass


    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")