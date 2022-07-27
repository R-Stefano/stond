from datetime import datetime
import LoggerManager
import sensors
import RPi.GPIO as gpio # allo to call GPIO pins

gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)
logger = LoggerManager.logger

class FanActuator():
    def __init__(self):
        # Internal Variables
        self.BOTTOM_FAN_PIN = 12 # GPIO12 PWM0 (Physical PIN 32)
        self.TOP_FAN_PIN = 13 # GPIO13 PWM0 (Physical PIN 33)
        self.PWM_FREQ = 100 # [kHz] 25kHz for Noctua PWM control
        self.MIN_TEMP = 24
        self.MAX_TEMP = 28
        self.FAN_OFF = 0 
        self.FAN_MAX = 100
        self.BACKUP_SPEED = 50 # In case can't read Temp - use this speed

        #Public variables 
        self.status = "OFF" #TODO: DEPRECATED
        self.isWorking = False
        self.speed_top = 0
        self.speed_bottom = 0

        # Startup Fans
        self.start()

    def start(self):
        try:
            gpio.setup(self.BOTTOM_FAN_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            gpio.setup(self.TOP_FAN_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF

            self.fan_bottom = gpio.PWM(self.BOTTOM_FAN_PIN, self.PWM_FREQ)
            self.fan_top = gpio.PWM(self.TOP_FAN_PIN, self.PWM_FREQ)

            self.fan_bottom.start(0)
            self.fan_top.start(0)

            self.setFanSpeed(100, "bottom") # Harcode to max at the moment

            self.isWorking = True
        except Exception as e:
            logger.info("[FAN] Not working")
            logger.error(e)
            self.isWorking = False

    def setFanSpeed(self, speed, fanName):
        print(speed, fanName)
        speed = round(speed, 2)

        if (fanName == "top"):
            self.fan_top.ChangeDutyCycle(speed)
            self.speed_top = speed
        elif (fanName == "bottom"):
            self.fan_bottom.ChangeDutyCycle(speed)
            self.speed_bottom = speed

        if (speed == 0):
            self.status = "OFF" #TODO: DEPRECATED
        else:
            self.status = "ON" #TODO: DEPRECATED

        logger.debug("[FAN] Update Speed")

    def controlFanSpeed(self, fanName = "top", overrideAction = None):
        if (not self.isWorking):
            self.start()

        if (overrideAction != None):
            self.setFanSpeed(overrideAction, fanName)
            return

        # If anomaly with Temp Sensor - Set fixed speed
        if (not sensors.environment.temperatureHumiditySensorWorking):
            logger.debug("[FAN] Temp Sensor not working. Setting emergency speed")
            self.setFanSpeed(self.BACKUP_SPEED, fanName)
            return

        currentTemp = sensors.environment.temperature
        if currentTemp < self.MIN_TEMP: # Set fan speed to MINIMUM if the temperature is below MIN_TEMP
            self.setFanSpeed(self.FAN_OFF, fanName)
        elif currentTemp > self.MAX_TEMP: # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
            self.setFanSpeed(self.FAN_MAX, fanName)
        else: # Caculate dynamic fan speed
            powerPerc = (currentTemp - self.MIN_TEMP)/(self.MAX_TEMP - self.MIN_TEMP) # get number between 0 and 1
            self.setFanSpeed(powerPerc * 100, fanName)

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

class HeaterActuator():
    def __init__(self):
        # Internal Variables
        self.HEATER_RELAY_GPIO_PIN = 20
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
            logger.info("[HEATER] not working")
            logger.error(e)
            self.isWorking = False

    def controlTemperature(self, overrideAction = None):
        if (not self.isWorking):
            self.start()

        currentTemp = sensors.environment.temperature

        if currentTemp < self.MIN_TEMP: # Turn on the heater if box below min temperature
            self.status = "ON"
            gpio.output(self.HEATER_RELAY_GPIO_PIN, gpio.HIGH)
        elif currentTemp > self.MAX_TEMP: # Turn off the heater if box below min temperature
            self.status = "OFF"
            gpio.output(self.HEATER_RELAY_GPIO_PIN, gpio.LOW)
        else:
            self.status = "OFF"
            gpio.output(self.HEATER_RELAY_GPIO_PIN, gpio.LOW)


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

'''

humidifier = Humidifier()

def humidity(humidity):
    if (humidity > 80):
        humidifier.turnOff()
    else:
        humidifier.turnOn()
'''

ventilation = FanActuator()
led = LightsActuator()
heater = HeaterActuator()