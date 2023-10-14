import busio, digitalio, board
import time
import sys
sys.path.insert(1,'/home/pi/stond/pi')
import main

import adafruit_mcp3xxx.mcp3008 as MCP

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

        in_min = float(main.config.get('ph_sensor', 'param2'))
        in_max = float(main.config.get('ph_sensor', 'param1')) 
        ph = round((raw_ph - in_min)*(7-4)/(in_max-in_min) + 4, 2)
        print("ph value: ",ph)
        print("ph volt: ",raw_ph)

    except Exception as e:
        print("[MCP3008] (start) Not working. E201-C-BNC OR TDS Sensor not working")
        print(e)
    time.sleep(2)

