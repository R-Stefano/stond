from gpiozero import CPUTemperature
import busio, digitalio, board, RPi # General librariers
import glob, subprocess, time, os # General librariers
import logger, configs # Internal libraries
from unittest.mock import MagicMock

# PH SENSOR
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


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
        self.temperatureHumiditySensorWorking = False

        self.temperature = None
        self.humidity = None

        self.address = 0x77
        try:
            #self.bmp = BMP085(self.address)
            self.temperatureHumiditySensorWorking = True
        except Exception as e:
            logger.add("info", "\n\nSome error while loading BME280 sensor\n\n")
            logger.add("error", e)
            self.temperatureHumiditySensorWorking = False

    def readTempHumidity(self):
        try:
            self.humidity = None
            self.temperature = 19 #self.bmp.readTemperature()
        except Exception as e:
            logger.add("info", "Some error while trying to read Temp & Humidity Dat")
            logger.add("error", e)
            self.humidity = None
            self.temperature = None
            self.temperatureHumiditySensorWorking = False

# Water Temp
class WaterSensor():
    def __init__(self):
        self.temperatureSensorWorking = False
        self.levelSensorWorking = False
        self.phSensorWorking = False

        self.temperature = None
        self.level = None
        self.ph = None

        self.WATER_LEVEL_PIN = 15
        # Software SPI configuration: PH SENSOR

        try:
            base_dir = '/sys/bus/w1/devices/'
            device_folder = glob.glob(base_dir + '28*')[0]
            self.device_file = device_folder + '/w1_slave'
            self.temperatureSensorWorking = True
        except Exception as e:
            logger.add("info", "\n\nSome error during Water Temp Sensor (DS18B20) setup\n\n")
            logger.add("error", e)
            self.temperatureSensorWorking = False
        
        try:
            RPi.GPIO.setup(self.WATER_LEVEL_PIN, RPi.GPIO.IN)
            self.levelSensorWorking = True
        except Exception as e:
            logger.add("info", "\n\nSome error during Water Level Sensor setup\n\n")
            logger.add("error", e)
            self.levelSensorWorking = False

        # PH SENSORS
        try:
            # create the spi bus
            spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI)
            # create the cs (chip select)
            cs = digitalio.DigitalInOut(board.D5) # PIN 24 GPIO10
            self.mcp = MCP.MCP3008(spi, cs)
            self.phSensorWorking = True
        except Exception as e:
            logger.add("info", "\n\nSome error during PH Sensor setup\n\n")
            logger.add("error", e)
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
        #  Output 1 if water touch the sensor
        _waterLevel = None
        if (self.levelSensorWorking):
            _waterLevel = int(RPi.GPIO.input(self.WATER_LEVEL_PIN))
        self.level = _waterLevel

    def getPh(self):
        _phValue = None
        if (self.phSensorWorking):
            channel = AnalogIn(self.mcp, MCP.P0) # 0 - 65472
            _phValue = (channel.value / 4365) #Map to 0 and 14 (included)
            print("hell0")
            print(self.mcp.read(0))
            print(channel.value, channel.voltage, (channel.value / 4365))
            print()

        self.ph = _phValue

cpu = Cpu()
environment = HumidityTempSensor()
water = WaterSensor()
