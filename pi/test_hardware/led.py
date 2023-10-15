from RPi import GPIO as gpio

import argparse
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

LED_RELAY_GPIO_PIN = 16

gpio.setmode (gpio.BCM)
gpio.setup(LED_RELAY_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with HUMIDIFIER OFF

try:
    if (args.action == "off"):
        gpio.output(LED_RELAY_GPIO_PIN, gpio.HIGH)
        print("[LED] Start Setup OFF")
    elif (args.action == "on"):
        gpio.output(LED_RELAY_GPIO_PIN, gpio.LOW)
        print("[LED] Start Setup ON")
    else:
        print("no action selected")
except Exception as e:
    print("[LED] not working")
    print(e)