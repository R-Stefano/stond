from RPi import GPIO as gpio

import argparse
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

HUMIDIFIER_GPIO_PIN = 25
while(1):
    try:
        print("[HUMIDIFIER] Start Initial Setup")

        if (args.action == "off"):
            gpio.output(HUMIDIFIER_GPIO_PIN, gpio.HIGH)
        elif (args.action == "on"):
            gpio.output(HUMIDIFIER_GPIO_PIN, gpio.LOW)
        else:
            print("no action selected")

    except Exception as e:
        print("[HUMIDIFIER] not working")
        print(e)