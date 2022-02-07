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

class System():
    def __init__(self):
        self.cpu_temperature = 0

        if (configs.debug):
            self._cpu = MagicMock()
            self._cpu.temperature = 0
        else:
            self._cpu = CPUTemperature()

    def read_cpu (self):
        self.cpu_temperature = self._cpu.temperature


# Humidity and Temp
class HumidityTempSensor():
    def __init__(self):
        # Internal Variables
        self._address = 0x77

        #Public variables 
        self.temperatureHumiditySensorWorking = False
        self.temperature = 0
        self.humidity = 0

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
            logger.info("[BME280] Impossible Reading Temp & Humidity")
            logger.error(e)
            self.humidity = 0
            self.temperature = 0
            self.temperatureHumiditySensorWorking = False

# Water Temp
class WaterSensor():
    def __init__(self):
        # Internal Variables
        self.WATER_LEVEL_PIN = 17 # GPIO 17 (Physical PIN 11)
        self.WATER_PH_PIN = board.D5 # GPIO5 (Physical PIN 29)
        self.MCP3008_PH_PIN = 0 # PIN on the MCP3008 Module for the PH Sensor

        #Public variables 
        self.phSensorWorking = False
        self.temperatureSensorWorking = False
        self.levelSensorWorking = False

        self.ph = 0
        self.temperature = 0
        self.level = 0

        # Start Sensors
        self.start_ph_sensor()
        self.start_waterTemp_sensor()
        self.start_waterLevel_sensor()


    def start_ph_sensor(self):
        try:
            spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
            cs = digitalio.DigitalInOut(self.WATER_PH_PIN) # PIN 29 GPIO5 - create the cs (chip select)
            self.mcp = MCP.MCP3008(spi, cs)
            self.phSensorWorking = True
        except Exception as e:
            logger.info("[E201-C-BNC] (start) Not working")
            logger.error(e)
            self.phSensorWorking = False

    def start_waterTemp_sensor(self):
        try:
            device_folder = glob.glob('/sys/bus/w1/devices/28*')[0]
            self.device_file = device_folder + '/w1_slave'
            self.temperatureSensorWorking = True
        except Exception as e:
            logger.info("[DS18B20] (start) Not working")
            logger.error(e)
            self.temperatureSensorWorking = False

    def start_waterLevel_sensor(self):
        try:
            gpio.setup(self.WATER_LEVEL_PIN, gpio.IN)
            self.levelSensorWorking = True
        except Exception as e:
            logger.info("[FS-IR02] (start) Not working")
            logger.error(e)
            self.levelSensorWorking = False

    def read_ph(self):
        # Used for mapping 0-1024 to ph value (0-14)
        range_in_start = 0
        range_in_end = 1024
        range_out_start = 0
        range_out_end = 14

        if (not self.phSensorWorking):
            self.start_ph_sensor()

        try:
            # map 0-1024 to 0-14
            self.ph = (self.mcp.read(self.MCP3008_PH_PIN) - range_in_start) * ((range_out_end - range_out_start)/(range_in_end - range_in_start)) + range_out_start
        except Exception as e:
            logger.info("[E201-C-BNC] Impossible Reading PH")
            logger.error(e)
            self.ph = 0
            self.phSensorWorking = False

        return self.ph

    def _read_temp_raw(self):
        catdata = subprocess.Popen(['cat', self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

    def read_temperature(self):
        if (not self.temperatureSensorWorking):
            self.start_waterTemp_sensor()

        try:
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
        except Exception as e:
            logger.info("[DS18B20] Impossible Reading Temperature")
            logger.error(e)
            self.temperature = 0
            self.temperatureSensorWorking = False


    def read_level(self):
        if (not self.levelSensorWorking):
            self.start_waterLevel_sensor()

        #  Output 1 if water touch the sensor
        try: 
            self.level = int(gpio.input(self.WATER_LEVEL_PIN))
        except Exception as e:
            logger.info("[FS-IR02] Impossible Reading Water Level")
            logger.error(e)
            self.level = 0
            self.levelSensorWorking = False

system = System()
environment = HumidityTempSensor()
water = WaterSensor()
