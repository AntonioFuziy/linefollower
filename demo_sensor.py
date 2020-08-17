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

#functions for moving the robot
def forward(delay):
    gpio.output(pin1, True)
    gpio.output(pin2, False)

    gpio.output(pin3, True)
    gpio.output(pin4, False)

    time.sleep(delay)
    gpio.cleanup()

def right(delay):
    gpio.output(pin1, True)
    gpio.output(pin2, True)

    gpio.output(pin3, True)
    gpio.output(pin4, False)

    time.sleep(delay)
    gpio.cleanup()

def left(delay):
    gpio.output(pin1, True)
    gpio.output(pin2, False)

    gpio.output(pin3, True)
    gpio.output(pin4, True)

    time.sleep(delay)
    gpio.cleanup()

def backwards(delay):
    gpio.output(pin1, False)
    gpio.output(pin2, True)

    gpio.output(pin3, False)
    gpio.output(pin4, True)

    time.sleep(delay)
    gpio.cleanup()

def stop(delay):
    gpio.output(pin1, True)
    gpio.output(pin2, True)

    gpio.output(pin3, True)
    gpio.output(pin4, True)

    time.sleep(delay)
    gpio.cleanup()

#going forward
if gpio.input(pin5) == True and gpio.input(pin6) == True:
    forward(delay)

#turning right
elif gpio.input(pin5) == False and gpio.input(pin6) == True:
    right(delay)

#turning left
elif gpio.input(pin5) == True and gpio.input(pin6) == False:
    left(delay)

#stopping
else:
    stop(delay)