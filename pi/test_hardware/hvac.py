from RPi import GPIO as gpio

import argparse
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

HVAC_MODE_GPIO_PIN = 24 # GPIO23
HVAC_START_GPIO_PIN = 23 # GPIO24

gpio.setmode (gpio.BCM)
gpio.setup(HVAC_MODE_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(HVAC_START_GPIO_PIN, gpio.OUT, initial=gpio.LOW)

try:
    params = args.action.split(":")
    state = params[0] 
    mode = params[1]
    if (state == "off"):
        gpio.output(HVAC_START_GPIO_PIN, gpio.LOW)
        print("[HVAC] Start Setup OFF")
    elif (state == "on"):
        gpio.output(HVAC_START_GPIO_PIN, gpio.HIGH)
        print("[HVAC] Start Setup ON")
    else:
        print("no action selected")

    if (mode == "hot"):
        gpio.output(HVAC_MODE_GPIO_PIN, gpio.LOW)
        print("[HVAC] Start Setup HOT")
    elif(mode == "cold"):
        gpio.output(HVAC_MODE_GPIO_PIN, gpio.HIGH)
        print("[HVAC] Start Setup COLD")
    else:
        print("no mode selected")

except Exception as e:
    print("[HVAC] not working")
    print(e)