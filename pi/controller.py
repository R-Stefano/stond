from datetime import datetime
import LoggerManager
import sensors
import RPi.GPIO as gpio # allo to call GPIO pins

gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)
logger = LoggerManager.logger

class FanActuator():
    def __init__(self):
        # Internal Variables
        self.FAN_PIN = 12 # GPIO12 PWM0 (Physical PIN 32)
        self.PWM_FREQ = 25 # [kHz] 25kHz for Noctua PWM control
        self.MIN_TEMP = 20 
        self.MAX_TEMP = 27
        self.FAN_OFF = 0 
        self.FAN_MAX = 100
        self.BACKUP_SPEED = 50 # In case can't read Temp - use this speed

        #Public variables 
        self.status = "OFF"
        self.isWorking = False
        self.speed = self.FAN_OFF

        # Startup Fans
        self.start()

    def start(self):
        try:
            gpio.setup(self.FAN_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            self.fan = gpio.PWM(self.FAN_PIN, self.PWM_FREQ)
            self.fan.start(self.FAN_OFF)
            self.isWorking = True
        except Exception as e:
            logger.info("[FAN] Not working")
            logger.error(e)
            self.isWorking = False

    def setFanSpeed(self, speed):
        self.speed = speed
        self.fan.start(self.speed)

        if (speed == 0):
            self.status = "OFF"
        else:
            self.status = "ON"

        logger.debug("[FAN] (update speed) Speed {} - Status {}".format(self.speed, self.status))

    def controlFanSpeed(self, overrideAction = None):
        if (not self.isWorking):
            self.start()

        if (overrideAction != None):
            self.setFanSpeed(overrideAction)
            return

        # If anomaly with Temp Sensor - Set fixed speed
        if (not sensors.environment.temperatureHumiditySensorWorking):
            logger.debug("[FAN] Temp Sensor not working. Setting emergency speed")
            self.setFanSpeed(self.BACKUP_SPEED)
            return

        currentTemp = sensors.environment.temperature
        if currentTemp < self.MIN_TEMP: # Set fan speed to MINIMUM if the temperature is below MIN_TEMP
            self.setFanSpeed(self.FAN_OFF)
        elif currentTemp > self.MAX_TEMP: # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
            self.setFanSpeed(self.FAN_MAX)
        else: # Caculate dynamic fan speed
            powerPerc = (currentTemp - self.MIN_TEMP)/(self.MAX_TEMP - self.MIN_TEMP) # get number between 0 and 1
            self.setFanSpeed(powerPerc * 100)

class LightsActuator():
    def __init__(self):
        # Internal Variables
        self.LED_RELAY_GPIO_PIN = 16

        self.CLOCK_TIMEZONE = 'UK' # NOT IMPLEMENTED 
        self.HOURS_LIGHT = 16
        self.HOUR_LIGHT_START = 12
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
            gpio.setup(self.LED_RELAY_GPIO_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            self.isWorking = True
        except Exception as e:
            logger.info("[LED] not working")
            logger.error(e)
            self.isWorking = False

    def controlLights(self, overrideAction = None):
        if (not self.isWorking):
            self.start()

        currentHr = datetime.utcnow().hour #UTC TIMEZONE

        if (overrideAction and overrideAction == "ON"):
            self.status = "ON"
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.HIGH)
        elif (overrideAction and overrideAction == "OFF"):
            self.status = "OFF"
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.LOW)
        elif (overrideAction == None and currentHr in self.LIGHT_HOURS):
            self.status = "ON"
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.HIGH)
        else:
            self.status = "OFF"
            gpio.output(self.LED_RELAY_GPIO_PIN, gpio.LOW)

'''

class Humidifier():
    def __init__(self):
        self.status = "OFF"
        self.isWorking = False
        self.HUMIDIFIER_GPIO_PIN = 27
        try:
            RPi.GPIO.setup(self.HUMIDIFIER_GPIO_PIN, RPi.GPIO.OUT)
            RPi.GPIO.output(self.HUMIDIFIER_GPIO_PIN, RPi.GPIO.LOW)
            self.isWorking = True
        except Exception as e:
            logger.add("info", "Humidifier not working")
            logger.add("error", e)

    def turnOn(self):
        self.status = "ON"
        RPi.GPIO.output(self.HUMIDIFIER_GPIO_PIN, RPi.GPIO.HIGH)
        return

    def turnOff(self):
        self.status = "OFF"
        RPi.GPIO.output(self.HUMIDIFIER_GPIO_PIN, RPi.GPIO.LOW)
        return
'''
ventilation = FanActuator()
led = LightsActuator()
'''

humidifier = Humidifier()

def humidity(humidity):
    if (humidity > 80):
        humidifier.turnOff()
    else:
        humidifier.turnOn()
'''
