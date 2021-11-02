from gpiozero import CPUTemperature
import bme280
import smbus2
import glob, subprocess, time, os
import RPi # allo to call GPIO pins
import logger
import configs
from unittest.mock import MagicMock
import busio, digitalio
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
class Bme280():
    def __init__(self):
        self.working = False
        port = 1
        self.address = 0x77
        try:
            self.bus = smbus2.SMBus(port)
            self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
            self.working = True
        except Exception as e:
            logger.add("info", "Some error while loading BME280 sensor")
            logger.add("error", e)
            self.working = False
    
        if (configs.debug):
            self.working = True
            _bme280 = MagicMock()
            responseObject = MagicMock()
            responseObject.humidity = 0
            responseObject.temperature = 0
            _bme280.sample = MagicMock(return_value=responseObject)

    def readTempHumidity(self):
        snapshot = {
                'humidity': None,
                'temperature': None
            }

        if (configs.debug):
            return 0, 0

        if not self.working:
            return snapshot['temperature'], snapshot['humidity']

        try:
            data = bme280.sample(self.bus, self.address, self.calibration_params)
            snapshot['humidity'] = data.humidity
            snapshot['temperature'] = data.temperature
        except Exception as e:
            logger.add("info", "Some error while trying to read Temp & Humidity Dat")
            logger.add("debug", os.system('i2cdetect -y 1'))
            logger.add("error", e)
        finally:
            return snapshot['temperature'], snapshot['humidity']

# Water Temp
class WaterSensor():
    def __init__(self):
        self.temperatureSensorWorking = False
        self.levelSensorWorking = False
        self.phSensorWorking = False

        self.WATER_LEVEL_PIN = 17
        # Software SPI configuration: PH SENSOR

        try:
            base_dir = '/sys/bus/w1/devices/'
            device_folder = glob.glob(base_dir + '28*')[0]
            self.device_file = device_folder + '/w1_slave'
            self.temperatureSensorWorking = True
        except Exception as e:
            logger.add("info", "Some error during Water Temp Sensor setup")
            logger.add("error", e)
            self.temperatureSensorWorking = False
        
        try:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setup(self.WATER_LEVEL_PIN, RPi.GPIO.IN)
            self.levelSensorWorking = True
        except Exception as e:
            logger.add("info", "Some error during Water Level Sensor setup")
            logger.add("error", e)
            self.levelSensorWorking = False

        try:
            CLK  = 18
            MISO = 23
            MOSI = 24
            CS   = 25

            spi = busio.SPI(clock=CLK, MISO=MISO, MOSI=MOSI)
            cs = digitalio.DigitalInOut(CS)
            self.mcp = MCP.MCP3008(spi, cs)
            self.phSensorWorking = True
        except Exception as e:
            logger.add("info", "Some error during PH Sensor setup")
            logger.add("error", e)
            self.phSensorWorking = False

    def _read_temp_raw(self):
        catdata = subprocess.Popen(['cat', self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

    @property
    def temperature(self):
        temp_c = None
        if (configs.debug):
            return 0

        if (not self.temperatureSensorWorking):
            return None
    
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

    @property
    def level(self):
        #  Output 1 if water touch the sensor
        if (configs.debug):
            return 0

        if (not self.levelSensorWorking):
            return None

        return int(RPi.GPIO.input(self.WATER_LEVEL_PIN))

    @property
    def ph(self):
        if (configs.debug):
            return 7

        if (not self.phSensorWorking):
            return None

        channel = AnalogIn(self.mcp, MCP.P0)
        print('Raw ADC Value: ', channel.value)

        return 7

cpu = Cpu()
environment = Bme280()
water = WaterSensor()
