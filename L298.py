import RPi.GPIO as gpio
import time

pin1 = 1  #numero do pino da raspberry
pin2 = 2  #numero do pino da raspberry
pin3 = 3
pin4 = 4

#enA = 
#enB = 

delay = 3 #delay do motor ao enviar sinal

gpio.setmode(gpio.BCM)
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)

gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

gpio.setup(enA, gpio.OUT)
gpio.setup(enB, gpio.OUT)

def forward(delay):
    gpio.output(pin1, False)
    gpio.output(pin2, True)
    tim.sleep(delay)
    gpio.cleanup()

def backwards(delay):
    gpio.output(pin1, True)
    gpio.output(pin2, False)
    time.sleep(delay)
    gpio.cleanup()

#going forward
#forward(delay)

#going backwards
#backwards(dela)