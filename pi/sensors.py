from tkinter import E
import gpiozero
import busio, digitalio, board # General librariers
import glob, subprocess, time, os # General librariers
from unittest.mock import MagicMock
from datetime import datetime
import socket
import main

# PH SENSOR
import adafruit_mcp3xxx.mcp3008 as MCP

# BME280 SENSOR
from adafruit_bme280 import basic as adafruit_bme280

# CAMERA
from picamera import PiCamera

from RPi import GPIO as gpio # allow to call GPIO pins

import LoggerManager
gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)
logger = LoggerManager.logger

class System():
    def __init__(self):
        self.cpu_temperature = 0
        self.cpu = gpiozero.CPUTemperature()
        self.cameraSnapshotsDirPath = os.path.join(os.path.dirname(__file__), 'snapshots/')
        self.cpuSensorWorking = True

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        self.ip = s.getsockname()[0]

        # Setup camera
        try:
            # Create storage folder
            if (not os.path.exists(self.cameraSnapshotsDirPath)):
                logger.debug("[CAMERA] snapshot folder does not exist - creating one")
                os.mkdir(self.cameraSnapshotsDirPath)
                
            self.camera = PiCamera()
            self.camera.resolution = (2592, 1944)
                
            self.cameraWorking = True
        except Exception as e:
            logger.info("[CAMERA] (start) Not working")
            logger.error(e)
            self.cameraWorking = False

    def read_cpu (self):
        logger.debug("[SYSTEM] Reading CPU")
        self.cpu_temperature = self.cpu.temperature

    def take_picture(self):
        logger.debug("[SYSTEM] Camera Snapshot")
        try :
            self.camera.start_preview()
            time.sleep(5)
            self.camera.capture('/home/pi/stond/pi/snapshots/' + datetime.utcnow().isoformat() + '.jpg')
            self.camera.stop_preview()
        except Exception as e:
            logger.info("[CAMERA] Impossible Take Photo")
            logger.error(e)

# Humidity and Temp
class HumidityTempSensor():
    def __init__(self):
        # Internal Variables
        self._address = 0x76

        #Public variables 
        self.temperatureHumiditySensorWorking = False
        self.temperature = 0
        self.humidity = 0

        # Startup Sensor
        self.start()

    def start(self):
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, self._address)
            self.temperatureHumiditySensorWorking = True
        except Exception as e:
            logger.info("[BME280] (start) Not working")
            logger.error(e)
            self.temperatureHumiditySensorWorking = False

    def readTempHumidity(self):
        logger.debug("[BME280] Reading Temp & Humidity")
        if (not self.temperatureHumiditySensorWorking):
            self.start()

        try:
            self.humidity = round(self.bme280.humidity, 2)
            self.temperature = round(self.bme280.temperature, 2)
        except Exception as e:
            logger.info("[BME280] Impossible Reading Temp & Humidity")
            logger.error(e)
            self.humidity = 0
            self.temperature = 0
            self.temperatureHumiditySensorWorking = False

        return self.temperature, self.humidity

# Water Temp
class WaterSensor():
    def __init__(self):
        # Internal Variables
        self.WATER_LEVEL_PIN = 17 # GPIO 17 (Physical PIN 11)
        self.WATER_PH_PIN = board.D5 # GPIO5 (Physical PIN 29)
        self.MCP3008_PH_PIN = 0 # PIN on the MCP3008 Module for the PH Sensor
        self.MCP3008_EC_PIN = 1 # PIN on the MCP3008 Module for the EC Sensor

        #Public variables 
        self.phSensorWorking = False
        self.temperatureSensorWorking = False
        self.levelSensorWorking = False
        self.ecSensorWorking = False

        self.ph = 0 #Calibrated ph value
        self.raw_ph = 0 # Value coming out of the sensor
        self.ec = 0
        self.temperature = 0
        self.level = 0

        # Start Sensors
        self.start_ph_ec_sensor()
        self.start_waterTemp_sensor()
        self.start_waterLevel_sensor()


    def start_ph_ec_sensor(self):
        try:
            spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
            cs = digitalio.DigitalInOut(self.WATER_PH_PIN) # PIN 29 GPIO5 - create the cs (chip select)
            self.mcp = MCP.MCP3008(spi, cs)
            self.phSensorWorking = True
            self.ecSensorWorking = True
        except Exception as e:
            logger.info("[MCP3008] (start) Not working. E201-C-BNC OR TDS Sensor not working")
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

    def get_raw_ph(self):
        logger.debug("[E201-C-BNC] Reading PH")

        if (not self.phSensorWorking):
            self.start_ph_ec_sensor()

        try:
            self.raw_ph = self.mcp.read(self.MCP3008_PH_PIN)
            # map 0-1024 to 0-14
        except Exception as e:
            logger.info("[E201-C-BNC] Impossible Reading PH")
            logger.error(e)
            self.raw_ph = 0
            self.ph = 0
            self.phSensorWorking = False
        return self.raw_ph

    def read_ph(self):
        self.get_raw_ph()
        #self.ph = abs(round(float(main.config.get('ph_sensor', 'param1')) * self.raw_ph + float(main.config.get('ph_sensor', 'param2')), 2))
        self.ph = round(float(main.config.get('ph_sensor', 'param1')) * (float(main.config.get('ph_sensor', 'param2')) - self.raw_ph) + 4, 2)
        return self.ph

    def read_ppm(self):
        logger.debug("[EC] Reading PPM")
        if (not self.ecSensorWorking):
            self.start_ph_ec_sensor()

        try:
            self.ec = round(self.mcp.read(self.MCP3008_EC_PIN), 2)
        except Exception as e:
            logger.info("[EC] Reading EC")
            logger.error(e)
            self.ec = 0
            self.ecSensorWorking = False

        return self.ec

    def _read_temp_raw(self):
        catdata = subprocess.Popen(['cat', self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

    def read_temperature(self):
        logger.debug("[DS18B20] Reading Water Temperature")

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
                temp_c = (float(temp_string) / 1000.0)
                temp_f = temp_c * 9.0 / 5.0 + 32.0
            self.temperature = temp_c
        except Exception as e:
            logger.info("[DS18B20] Impossible Reading Temperature")
            logger.error(e)
            self.temperature = 0
            self.temperatureSensorWorking = False

        return self.temperature

    def read_level(self):
        logger.debug("[FS-IR02] Reading Water level")

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

        return self.level

system = System()
environment = HumidityTempSensor()
water = WaterSensor()
