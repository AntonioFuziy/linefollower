import RPi.GPIO as gpio
import time

pin1 = 1  #(PIN 1 - Motor DC direito A)
pin2 = 2  #(PIN 2 - Motor DC direito B)
pin3 = 3  #(PIN 3 - Motor DC esquerdo A)
pin4 = 4  #(PIN 4 - Motor DC esquerdo B)
pin5 = 5  #(PIN 5 - Sensor esquerdo)
pin6 = 6  #(PIN 6 - Sensor direito)

delay = 1

gpio.setmode(gpio.BCM)

gpio.setup(pin1, gpio.OUT)  #Motor direito terminal A
gpio.setup(pin2, gpio.OUT)  #Motor direito terminal B

gpio.setup(pin3, gpio.OUT)  #Motor esquerdo terminal A
gpio.setup(pin4, gpio.OUT)  #Motor esquerdo terminal B

gpio.setup(pin5, gpio.IN)   #Entrada do sensor direito
gpio.setup(pin6, gpio.IN)   #Entrada do sensor esquerdo

class Direction:
    def __init__(self, delay, pinList, conditionList):
        self.delay = delay
        self.pinList = pinList
        self.conditionList = conditionList

    def moving(self):
        gpio.output(self.pinList[0], self.conditionList[0])
        gpio.output(self.pinList[1], self.conditionList[1])

        gpio.output(self.pinList[2], self.conditionList[2])
        gpio.output(self.pinList[3], self.conditionList[3])

        time.sleep(self.delay)
        gpio.cleanup()

#Instances for moving the robot
forward   = Direction(delay, [pin1, pin2, pin3, pin4], [True, False, True, False])
right     = Direction(delay, [pin1, pin2, pin3, pin4], [True, True, True, False])
left      = Direction(delay, [pin1, pin2, pin3, pin4], [True, False, True, True])
backwards = Direction(delay, [pin1, pin2, pin3, pin4], [False, True, False, True])
stop      = Direction(delay, [pin1, pin2, pin3, pin4], [True, True, True, True])

#going forward
if gpio.input(pin5) == True and gpio.input(pin6) == True:
    forward.moving()

#turning right
elif gpio.input(pin5) == False and gpio.input(pin6) == True:
    right.moving()

#turning left
elif gpio.input(pin5) == True and gpio.input(pin6) == False:
    left.moving()

#stopping
else:
    stop.moving()
