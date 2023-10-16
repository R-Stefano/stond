import busio, digitalio, board
import time, os

import adafruit_mcp3xxx.mcp3008 as MCP

from configparser import ConfigParser
config = ConfigParser()
config.read(os.path.join('/home/pi/stond/pi', 'config.ini'))

import argparse
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

WATER_PH_PIN = board.D5 # GPIO5 (Physical PIN 29)
MCP3008_PH_PIN = 0 # PIN on the MCP3008 Module for the PH Sensor

print("[E201-C-BNC] Reading PH")
while(1):
    try:
        spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
        cs = digitalio.DigitalInOut(WATER_PH_PIN) # PIN 29 GPIO5 - create the cs (chip select)
        mcp = MCP.MCP3008(spi, cs)

        try:
            raw_ph = mcp.read(MCP3008_PH_PIN)
            # map 0-1024 to 0-14
        except Exception as e:
            print("[E201-C-BNC] Impossible Reading PH")
            print(e)
        if (args.action == "on"):
            raw_ph = raw_ph+310
        in_min = float(config.get('ph_sensor', 'param2'))
        in_max = float(config.get('ph_sensor', 'param1')) 
        ph = round((raw_ph - in_min)*(7-4)/(in_max-in_min) + 4, 2)
        print("ph value: ",ph)
        print("ph volt: ",raw_ph)

    except Exception as e:
        print("[MCP3008] (start) Not working. E201-C-BNC OR TDS Sensor not working")
        print(e)
    time.sleep(2)

