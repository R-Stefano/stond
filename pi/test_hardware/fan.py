from RPi import GPIO as gpio

import argparse
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

FAN1_PIN = 13 # GPIO13 PWM0 (Physical PIN 32) - velocity control for fan BOTTOM
FAN1_ENABLER_PIN = 27 # GPIO27 (Physical PIN 13) - ON/OFF control for fan 1 
FAN2_PIN = 12 # GPIO12 PWM0 (Physical PIN 33) - velocity control for fan TOP
FAN2_ENABLER_PIN = 22 # GPIO22 (Physical PIN 15) - ON/OFF control for fan 2 

PWM_FREQ = 100 # [kHz] 25kHz for Noctua PWM control

gpio.setmode (gpio.BCM)
gpio.setup(FAN1_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(FAN1_ENABLER_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(FAN2_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(FAN2_ENABLER_PIN, gpio.OUT, initial=gpio.LOW)
fan1 = gpio.PWM(FAN1_PIN, PWM_FREQ)
fan2 = gpio.PWM(FAN2_PIN, PWM_FREQ)


params = args.action.split(":")
fan = params[0] 
speed = params[1]
speed = round(speed, 2)

if(fan == "fan1"):
    try:
        fan1.ChangeDutyCycle(speed)
        if (speed == 0):
            print("fan1 OFF")
            gpio.output(FAN1_ENABLER_PIN, gpio.LOW)
        else:
            print("fan1 vel: ",speed,"%")
            gpio.output(FAN1_ENABLER_PIN, gpio.HIGH)
    except Exception as e:
        print("[FAN1] not working")
        print(e)

elif(fan == "fan2"):
    try:
        fan2.ChangeDutyCycle(speed)
        if (speed == 0):
            print("fan2 OFF")
            gpio.output(FAN2_ENABLER_PIN, gpio.LOW)
        else:
            print("fan2 vel: ",speed,"%")
            gpio.output(FAN2_ENABLER_PIN, gpio.HIGH)

    except Exception as e:
        print("[FAN2] not working")
        print(e)

else:
    print("no fan selected")

