from tkinter import E
from gpiozero import CPUTemperature
import busio, digitalio, board # General librariers
import glob, subprocess, time, os # General librariers
import configs # Internal libraries
from unittest.mock import MagicMock

# PH SENSOR
import adafruit_mcp3xxx.mcp3008 as MCP

import RPi.GPIO as gpio # allo to call GPIO pins
import LoggerManager
gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)
logger = LoggerManager.logger

class Cpu():
    def __init__(self):
        if (configs.debug):
            self._cpu = MagicMock()
            self._cpu.temperature = 0
        else:
            self._cpu = CPUTemperature()

    @property
    def temperature (self):
        return self._cpu.temperature


# Humidity and Temp
class HumidityTempSensor():
    def __init__(self):
        # Internal Variables
        self._address = 0x77

        #Public variables 
        self.temperatureHumiditySensorWorking = False
        self.temperature = None
        self.humidity = None

        # Startup Sensor
        self.start()

    def start(self):
        try:
            self.bmp = BMP085(self._address)
            self.temperatureHumiditySensorWorking = True
        except Exception as e:
            logger.info("[BME280] (start) Not working")
            logger.error(e)
            self.temperatureHumiditySensorWorking = False

    def readTempHumidity(self):
        if (not self.temperatureHumiditySensorWorking):
            self.start()

        try:
            self.humidity = self.bmp.readTemperature()
            self.temperature = self.bmp.readTemperature()
        except Exception as e:
            logger.info("Impossible Reading Temp & Humidity")
            logger.error(e)
            self.humidity = None
            self.temperature = None
            self.temperatureHumiditySensorWorking = False

# Water Temp
class WaterSensor():
    def __init__(self):
        # Internal Variables
        self.WATER_LEVEL_PIN = 15
        self.WATER_PH_PIN = board.D5
        print(board.D5)
        
        #Public variables 
        self.levelSensorWorking = False
        self.phSensorWorking = False
        self.temperatureSensorWorking = False

        self.level = None
        self.ph = None
        self.temperature = None

        # Software SPI configuration: PH SENSOR

        try:
            base_dir = '/sys/bus/w1/devices/'
            device_folder = glob.glob(base_dir + '28*')[0]
            self.device_file = device_folder + '/w1_slave'
            self.temperatureSensorWorking = True
        except Exception as e:
            #logger.add("info", "\n\nSome error during Water Temp Sensor (DS18B20) setup\n\n")
            #logger.add("error", e)
            self.temperatureSensorWorking = False

        # PH SENSORS
        self.start_ph_sensor()
        self.start_waterLevel_sensor()


    def start_ph_sensor(self):
        try:
            spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
            cs = digitalio.DigitalInOut(self.WATER_PH_PIN) # PIN 29 GPIO5 - create the cs (chip select)
            self.mcp = MCP.MCP3008(spi, cs)
            self.phSensorWorking = True
        except Exception as e:
            logger.info("[PH SENSOR] (start) Not working")
            logger.error(e)
            self.phSensorWorking = False

    def start_waterLevel_sensor(self):
        try:
            gpio.setup(self.WATER_LEVEL_PIN, gpio.IN)
            self.levelSensorWorking = True
        except Exception as e:
            logger.info("[WATER LEVEL SENSOR] (start) Not working")
            logger.error(e)
            self.levelSensorWorking = False

    def getPh(self):
        if (not self.phSensorWorking):
            self.start_ph_sensor()

        try:
            print("hell0")
            print(self.mcp.read(0))
            print()
            self.ph = 1
        except Exception as e:
            logger.info("Impossible Reading PH")
            logger.error(e)
            self.ph = None
            self.phSensorWorking = False

    def _read_temp_raw(self):
        catdata = subprocess.Popen(['cat', self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

    def getTemperature(self):
        temp_c = None

        if (self.temperatureSensorWorking):
            lines = self._read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self._read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0

        self.temperature = temp_c

    def getLevel(self):
        self.level = None

        if (not self.levelSensorWorking):
            self.start_waterLevel_sensor()

        #  Output 1 if water touch the sensor
        try: 
            self.level = int(gpio.input(self.WATER_LEVEL_PIN))
        except Exception as e:
            self.level = None
            self.levelSensorWorking = False

cpu = Cpu()
environment = HumidityTempSensor()
water = WaterSensor()
