from RPi import GPIO as gpio

import argparse, time
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

HUMIDIFIER_GPIO_PIN = 25
gpio.setmode (gpio.BCM)
gpio.setup(HUMIDIFIER_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with HUMIDIFIER OFF
print("[HUMIDIFIER] Start Setup")
try:

    if (args.action == "off"):
        gpio.output(HUMIDIFIER_GPIO_PIN, gpio.HIGH)
    elif (args.action == "on"):
        gpio.output(HUMIDIFIER_GPIO_PIN, gpio.LOW)
    else:
        print("no action selected")

except Exception as e:
    print("[HUMIDIFIER] not working")
    print(e)