from datetime import datetime
import LoggerManager
import sensors
from RPi import GPIO as gpio # allo to call GPIO pins


gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)
logger = LoggerManager.logger

class FanActuator():
    def __init__(self):
        # Internal Variables
        self.FAN1_PIN = 13 # GPIO13 PWM0 (Physical PIN 32) - velocity control for fan BOTTOM
        self.FAN1_ENABLER_PIN = 27 # GPIO27 (Physical PIN 13) - ON/OFF control for fan 1 
        self.FAN2_PIN = 12 # GPIO12 PWM0 (Physical PIN 33) - velocity control for fan TOP
        self.FAN2_ENABLER_PIN = 22 # GPIO22 (Physical PIN 15) - ON/OFF control for fan 2 

        self.PWM_FREQ = 100 # [kHz] 25kHz for Noctua PWM control
        self.MIN_HUM = 50
        self.MAX_HUM = 90
        self.BACKUP_SPEED = 50 # In case can't read Temp - use this speed

        #Public variables 
        self.fan1_isWorking = False
        self.fan1_speed = 0
        self.fan1_status = "OFF"
        self.fan2_isWorking = False
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

            self.fan1_isWorking = True
            self.fan2_isWorking = True
        except Exception as e:
            logger.info("[FAN] Not working")
            logger.error(e)
            self.fan1_isWorking = False
            self.fan2_isWorking = False

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

    def controlFanSpeed(self, fanName = "fan2", overrideAction = None):
        logger.debug("[{}] Start Control Routine".format(fanName.upper()))
        if (not self.fan1_isWorking or not self.fan2_isWorking):
            self.start()

        if (overrideAction != None):
            logger.debug("[{}] Override Action {}".format(fanName.upper(), overrideAction))
            self.setFanSpeed(fanName, overrideAction)
            return

        # If anomaly with Temp Sensor - Set fixed speed
        if (not sensors.environment.temperatureHumiditySensorWorking):
            logger.debug("[{}] Temp Sensor not working. Setting emergency speed".format(fanName.upper()))
            self.setFanSpeed(fanName, self.BACKUP_SPEED)
            return

        currentHum = sensors.environment.humidity
        if currentHum < self.MIN_HUM: # Set fan speed to MINIMUM if the temperature is below MIN_TEMP
            self.setFanSpeed(fanName, 0)
        elif currentHum > self.MAX_HUM: # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
            self.setFanSpeed(fanName, 100)
        else: # Caculate dynamic fan speed
            powerPerc = (currentHum - self.MIN_HUM)/(self.MAX_HUM - self.MIN_HUM) # get number between 0 and 1
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

        logger.debug("[LED] STATE Changed {} => {}".format(self.status, _newStatus))

        if (_newStatus == "OFF"):
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.HIGH)
        elif (_newStatus == "ON"):
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.LOW)

        self.status = _newStatus

class HVACActuator():
    def __init__(self):
        '''
        pin1 - set 0 => cold | 1 => hot
        HVAC_START_GPIO_PIN - set 0 => OFF  | 1 => ON
        '''
        # Internal Variables
        self.HVAC_MODE_GPIO_PIN = 23 # GPIO23
        self.HVAC_START_GPIO_PIN = 24 # GPIO24
        self.MIN_TEMP = 24
        self.MAX_TEMP = 28

        self._mode_to_signal = {
            'HEATER': gpio.LOW,
            'COOLER': gpio.HIGH
        }

        #Public variables 
        self.mode = "HEATER" # heater or cooler # Start with HVAC heater mode
        self.status = "OFF"
        self.isWorking = False

        # Startup LEDs
        self.start()

    def start(self):
        logger.info("[HVAC] Start Initial Setup")
        try:
            gpio.setup(self.HVAC_MODE_GPIO_PIN, gpio.OUT, initial=self._mode_to_signal[self.mode]) # set mode: 'cooler' or 'heater
            gpio.setup(self.HVAC_START_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with HVAC OFF

            self.isWorking = True
        except Exception as e:
            logger.info("[HVAC] not working")
            logger.error(e)
            self.isWorking = False

    def setMode(self, mode):
        '''
            set mode: 'cooler' or 'heater
        '''
        if (mode == self.mode):
            return
        
        gpio.output(self.HVAC_MODE_GPIO_PIN, self._mode_to_signal[mode])
        logger.debug("[HVAC] Mode Changed {} => {}".format(self.mode, mode))

        self.mode = mode

    def setStatus(self, status):
        '''
            set status : 'ON' or 'OFF'
        '''
        if (status == self.status):
            return
        
        if (status == "ON"):
            gpio.output(self.HVAC_START_GPIO_PIN, gpio.HIGH)
        else:
            gpio.output(self.HVAC_START_GPIO_PIN, gpio.LOW)

        logger.debug("[HVAC] State Changed {} => {}".format(self.status, status))
        self.status = status

    def controlTemperature(self, overrideAction = None):
        '''
        
        '''
        logger.debug("[HVAC] Start Control Routine")
        if (not self.isWorking):
            self.start()

        currentTemp = sensors.environment.temperature
        _newMode = self.mode
        _newStatus = self.status

        # Set HVAC on heater mode and turn it on
        if currentTemp < self.MIN_TEMP:  # Turn on heater if box below min temperature
            _newMode = "HEATER"
            _newStatus = "ON"
        elif currentTemp > self.MAX_TEMP: # Turn on cooler if box above max temperature
            _newMode = "COOLER"
            _newStatus = "ON"
        else:
            _newStatus = "OFF" # turn hvac off if box in temperature range

        if (overrideAction != None):
            logger.debug("[HVAC] Override Action {}".format(overrideAction))
            [_newStatus, _newMode] = overrideAction.upper().split(":")

        if (_newMode != self.mode):
            self.setMode(_newMode)

        if (_newStatus != self.status):
            self.setStatus(_newStatus)

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
        currentHumidity = sensors.environment.humidity
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

        logger.debug("[HUMIDIFIER] State Changed {} => {}".format(self.status, _newStatus))

        if (_newStatus == "OFF"):
            gpio.output(self.HUMIDIFIER_GPIO_PIN, gpio.HIGH)
        elif (_newStatus == "ON"):
            gpio.output(self.HUMIDIFIER_GPIO_PIN, gpio.LOW)

        self.status = _newStatus
        return self.status


ventilation = FanActuator()
led = LightsActuator()
hvac = HVACActuator()
humidifier = HumidityActuator()
