from datetime import datetime
import LoggerManager
import sensors
from RPi import GPIO as gpio # allo to call GPIO pins


gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)
logger = LoggerManager.logger

class FanActuator():
    def __init__(self):
        # Internal Variables
        self.FAN1_PIN = 12 # GPIO12 PWM0 (Physical PIN 32) - velocity control for fan BOTTOM
        self.FAN1_ENABLER_PIN = 27 # GPIO27 (Physical PIN 13) - ON/OFF control for fan 1 
        self.FAN2_PIN = 13 # GPIO13 PWM0 (Physical PIN 33) - velocity control for fan TOP
        self.FAN2_ENABLER_PIN = 22 # GPIO22 (Physical PIN 15) - ON/OFF control for fan 2 

        self.PWM_FREQ = 100 # [kHz] 25kHz for Noctua PWM control
        self.MIN_TEMP = 24
        self.MAX_TEMP = 28
        self.BACKUP_SPEED = 50 # In case can't read Temp - use this speed

        #Public variables 
        self.isWorking = False
        self.fan1_speed = 0
        self.fan1_status = "OFF"
        self.fan2_speed = 0
        self.fan2_status = "OFF"

        # Startup Fans
        self.start()

    def start(self):
        try:
            logger.info("[FAN] Start Initial Setup")
            #setup of PWM pins 
            gpio.setup(self.FAN1_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            gpio.setup(self.FAN1_ENABLER_PIN, gpio.OUT, initial=gpio.LOW)

            gpio.setup(self.FAN2_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            gpio.setup(self.FAN2_ENABLER_PIN, gpio.OUT, initial=gpio.LOW)

            self.fan1 = gpio.PWM(self.FAN1_PIN, self.PWM_FREQ)
            self.fan2 = gpio.PWM(self.FAN2_PIN, self.PWM_FREQ)

            self.fan1.start(0)
            self.fan2.start(0)

            self.setFanSpeed("fan1", 100)
            self.setFanSpeed("fan2", 0)

            self.isWorking = True
        except Exception as e:
            logger.info("[FAN] Not working")
            logger.error(e)
            self.isWorking = False

    def setFanSpeed(self, fanName, speed):
        '''
        fanName: fan1, fan2
        speed: 0 - 100
        '''
        speed = round(speed, 2)

        if (fanName == "fan1"):
            self.fan1.ChangeDutyCycle(speed)
            self.fan1_speed = speed
            if (speed == 0):
                self.fan1_status = "OFF"
                gpio.output(self.FAN1_ENABLER_PIN, gpio.LOW)
            else:
                self.fan1_status = "ON"
                gpio.output(self.FAN1_ENABLER_PIN, gpio.HIGH)
        elif (fanName == "fan2"):
            self.fan2.ChangeDutyCycle(speed)
            self.fan2_speed = speed
            if (speed == 0):
                self.fan2_status = "OFF"
                gpio.output(self.FAN2_ENABLER_PIN, gpio.LOW)
            else:
                self.fan2_status = "ON"
                gpio.output(self.FAN2_ENABLER_PIN, gpio.HIGH)

        logger.debug("[FAN] Control Routine - Update {} speed to {}%".format(fanName, speed))


    def controlFanSpeed(self, fanName = "fan2", overrideAction = None):
        logger.debug("[FAN] Start Control Routine")
        if (not self.isWorking):
            self.start()

        if (overrideAction != None):
            logger.debug("[FAN] Override Action {}".format(overrideAction))
            self.setFanSpeed(fanName, overrideAction)
            return

        # If anomaly with Temp Sensor - Set fixed speed
        if (not sensors.environment.temperatureHumiditySensorWorking):
            logger.debug("[FAN] Temp Sensor not working. Setting emergency speed")
            self.setFanSpeed(fanName, self.BACKUP_SPEED)
            return

        currentTemp = sensors.environment.temperature
        if currentTemp < self.MIN_TEMP: # Set fan speed to MINIMUM if the temperature is below MIN_TEMP
            self.setFanSpeed(fanName, 0)
        elif currentTemp > self.MAX_TEMP: # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
            self.setFanSpeed(fanName, 100)
        else: # Caculate dynamic fan speed
            powerPerc = (currentTemp - self.MIN_TEMP)/(self.MAX_TEMP - self.MIN_TEMP) # get number between 0 and 1
            self.setFanSpeed(fanName, int(powerPerc * 100))

class LightsActuator():
    def __init__(self):
        # Internal Variables
        self.LED_RELAY_GPIO_PIN = 16

        self.CLOCK_TIMEZONE = 'UK' # NOT IMPLEMENTED
        self.HOURS_LIGHT = 16
        self.HOUR_LIGHT_START = 7
        self.LIGHT_HOURS = []
        for i in range(self.HOURS_LIGHT):
            hour = self.HOUR_LIGHT_START + i
            hour = hour if hour < 24 else hour - 24
            self.LIGHT_HOURS.append(hour)

        #Public variables 
        self.status = "OFF"
        self.isWorking = False

        # Startup LEDs
        self.start()

    def start(self):
        try:
            logger.info("[LED] Start Initial Setup")
            gpio.setup(self.LED_RELAY_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            self.isWorking = True
        except Exception as e:
            logger.info("[LED] not working")
            logger.error(e)
            self.isWorking = False

    def controlLights(self, overrideAction = None):
        logger.debug("[LED] Start Control Routine")
        if (not self.isWorking):
            self.start()

        currentHr = datetime.utcnow().hour #UTC TIMEZONE
        _newStatus = self.status

        if (currentHr in self.LIGHT_HOURS):
            _newStatus = "ON"
        else:
            _newStatus = "OFF"

        if (overrideAction != None):
            logger.debug("[LED] Override Action {}".format(overrideAction))
            _newStatus = overrideAction.upper()

        if (self.status == _newStatus):
            return

        logger.debug("[LED] Control Routine - Update State {} => {}".format(self.status, _newStatus))

        if (_newStatus == "OFF"):
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.LOW)
        elif (_newStatus == "ON"):
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.HIGH)

        self.status = _newStatus

class HVACActuator():
    def __init__(self):
        '''
        pin1 - set 0 => cold | 1 => hot
        HVAC_START_GPIO_PIN - set 0 => OFF  | 1 => ON
        '''
        # Internal Variables
        self.HEATER_RELAY_GPIO_PIN = 23
        self.HVAC_START_GPIO_PIN = 24
        self.MIN_TEMP = 24
        self.MAX_TEMP = 28

        #Public variables 
        self.status = "OFF"
        self.isWorking = False

        # Startup LEDs
        self.start()

    def start(self):
        try:
            gpio.setup(self.HEATER_RELAY_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with HEATER OFF
            self.isWorking = True
        except Exception as e:
            logger.info("[HVAC] not working")
            logger.error(e)
            self.isWorking = False

    def controlTemperature(self, overrideAction = None):
        logger.debug("[HVAC] Try Update State")
        if (not self.isWorking):
            self.start()

        currentTemp = sensors.environment.temperature
        _newStatus = self.status

        if currentTemp < self.MIN_TEMP: # Turn on the heater if box below min temperature
            _newStatus = "ON"
        elif currentTemp > self.MAX_TEMP: # Turn off the heater if box above max temperature
            _newStatus = "OFF"

        if (overrideAction != None):
            logger.debug("[HVAC] Override Action {}".format(overrideAction))
            _newStatus = overrideAction.upper()

        if (_newStatus == "OFF"):
            gpio.output(self.HVAC_START_GPIO_PIN, gpio.LOW)
            gpio.output(self.HEATER_RELAY_GPIO_PIN, gpio.LOW)
        elif (_newStatus == "ON"):
            gpio.output(self.HVAC_START_GPIO_PIN, gpio.HIGH)
            gpio.output(self.HEATER_RELAY_GPIO_PIN, gpio.HIGH)

        self.status = _newStatus
    
        logger.debug("[HVAC] New State {}".format(self.status))

class HumidityActuator():
    def __init__(self):
        # Internal Variables
        self.HUMIDIFIER_GPIO_PIN = 25
        self.MIN_HUMIDITY = 60
        self.MAX_HUMIDITY = 90

        #Public variables 
        self.status = "ON"
        self.isWorking = False

        # Startup Humidifier
        self.start()

    def start(self):
        try:
            logger.info("[HUMIDIFIER] Start Initial Setup")
            gpio.setup(self.HUMIDIFIER_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with HUMIDIFIER OFF
            self.isWorking = True
        except Exception as e:
            logger.info("[HUMIDIFIER] not working")
            logger.error(e)
            self.isWorking = False

    def controlHumidity(self, overrideAction = None):
        logger.debug("[HUMIDIFIER] Start Control Routine")
        currentHumidity = sensors.environment.temperature
        _newStatus = self.status

        if (not self.isWorking):
            self.start()

        if currentHumidity < self.MIN_HUMIDITY: # Turn on the humidifier if box below min humidity
            _newStatus = "ON"
        elif currentHumidity > self.MAX_HUMIDITY: # Turn off the humidifier if box above max humidity
            _newStatus = "OFF"

        if (overrideAction != None):
            logger.debug("[HUMIDIFIER] Override Action {}".format(overrideAction))
            _newStatus = overrideAction.upper()

        if (self.status == _newStatus):
            return

        logger.debug("[HUMIDIFIER] Control Routing - Update State {} => {}".format(self.status, _newStatus))

        if (_newStatus == "OFF"):
            gpio.output(self.HUMIDIFIER_GPIO_PIN, gpio.HIGH)
        elif (_newStatus == "ON"):
            gpio.output(self.HUMIDIFIER_GPIO_PIN, gpio.LOW)

        self.status = _newStatus


ventilation = FanActuator()
led = LightsActuator()
hvac = HVACActuator()
humidifier = HumidityActuator()
