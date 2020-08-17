from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)

left_sensor = 11 #(pino)
right_sensor = 9 #(pino)

GPIO.setup(left_sensor, GPIO.IN) #(IN)
GPIO.setup(right_sensor, GPIO.IN) #(IN)

try:
    while True:
        #Se o sensor da direita sair da linha para direita, o robo de move para a esquerda
        if not GPIO.input(left_sensor):
            print("movendo para esquerda")

        #Se o sensor da esquerda sair da linha para esquerda, o robo de move para a direita
        elif not GPIO.input(right_sensor):
            print("movendo para a direita")

        #Case nenhuma condição seja verdade, continue reto
        else:
            print("andando reto")
        
        time.sleep(0.2)
except:
    GPIO.cleanup()