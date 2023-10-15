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

if(fan == "fan1"):
    try:
        if (speed == "low"):
            print("fan1 OFF")
            fan1.ChangeDutyCycle(0)
            gpio.output(FAN1_ENABLER_PIN, gpio.LOW)
        elif (speed == "medium"):
            fan1.ChangeDutyCycle(50)
            print("fan1 vel: 50%")
            gpio.output(FAN1_ENABLER_PIN, gpio.HIGH)
        elif (speed == "high"):
            fan1.ChangeDutyCycle(100)
            print("fan1 vel: 100%")
            gpio.output(FAN1_ENABLER_PIN, gpio.HIGH)
    except Exception as e:
        print("[FAN1] not working")
        print(e)

elif(fan == "fan2"):
    try:
        if (speed == "low"):
            fan2.ChangeDutyCycle(0)
            print("fan2 OFF")
            gpio.output(FAN2_ENABLER_PIN, gpio.LOW)
        elif (speed == "medium"):
            fan2.ChangeDutyCycle(50)
            print("fan2 vel: 50%")
            gpio.output(FAN2_ENABLER_PIN, gpio.HIGH)
        elif (speed == "high"):
            fan2.ChangeDutyCycle(100)
            print("fan2 vel: 100%")
            gpio.output(FAN2_ENABLER_PIN, gpio.HIGH)

    except Exception as e:
        print("[FAN2] not working")
        print(e)

else:
    print("no fan selected")

