from datetime import datetime
import logger, sensors
import RPi.GPIO as gpio # allo to call GPIO pins

gpio.setmode (gpio.BCM) # Use the Board Common pin numbers (GPIO)

class FanActuator():
    def __init__(self):
        self.status = "OFF"
        self.isWorking = False
        self.FAN_PIN = 26 # GPIO26 PWM0 (Physical PIN 32)
        self.PWM_FREQ = 25 # [kHz] 25kHz for Noctua PWM control

        # Internal Variables for the FAN Manager
        self.MIN_TEMP = 20 
        self.MAX_TEMP = 27
        self.FAN_OFF = 0 
        self.FAN_MAX = 100
        ## Try to Startup FAN
        try:
            gpio.setup(self.FAN_PIN, gpio.OUT, initial=gpio.LOW) # Start with FAN OFF
            self.fan = gpio.PWM(self.FAN_PIN, self.PWM_FREQ)
            self.fan.start(self.FAN_OFF)
            self.isWorking = True
        except Exception as e:
            logger.add("info", "[FAN] (start) Not working")
            logger.add("error", e)

    def setFanSpeed(self, speed):
        self.fan.start(speed)

        if (speed == 0):
            self.status = "OFF"
        else:
            self.status = "ON"

        #logger.add("debug", "[FAN] (update speed) Temp ${} - Speed ${} - Status ${}")

    def handleFanSpeed(self):
        # If anomaly with Temp Sensor - Set fixed speed
        if (not sensors.environment.temperatureHumiditySensorWorking):
            logger.add("debug", "[FAN] Temp Sensor not working. Setting emergency speed")
            self.setFanSpeed(25)
            return

        currentTemp = sensors.environment.temperature
        if currentTemp < self.MIN_TEMP: # Set fan speed to MINIMUM if the temperature is below MIN_TEMP
            self.setFanSpeed(self.FAN_OFF)
        elif currentTemp > self.MAX_TEMP: # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
            self.setFanSpeed(self.FAN_MAX)
        else: # Caculate dynamic fan speed
            powerPerc = (currentTemp - self.MIN_TEMP)/(self.MAX_TEMP - self.MIN_TEMP) # get number between 0 and 1
            self.setFanSpeed(powerPerc * 100)

'''
class LightsActuator():
    def __init__(self):
        self.status = "OFF"
        self.isWorking = False
        self.LED_RELAY_GPIO_PIN = 15
        try:
            RPi.GPIO.setup(self.LED_RELAY_GPIO_PIN, RPi.GPIO.OUT)
            RPi.GPIO.output(self.LED_RELAY_GPIO_PIN, RPi.GPIO.LOW)
            self.isWorking = True
        except Exception as e:
            logger.add("info", "Lights Actuator not working")
            logger.add("error", e)

    def turnOn(self):
        self.status = "ON"
        RPi.GPIO.output(self.LED_RELAY_GPIO_PIN, RPi.GPIO.HIGH)
        return

    def turnOff(self):
        self.status = "OFF"
        RPi.GPIO.output(self.LED_RELAY_GPIO_PIN, RPi.GPIO.LOW)
        return

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
'''

led = LightsActuator()
humidifier = Humidifier()

def lights():
    currentHr = datetime.utcnow().hour #UTC TIMEZONE
    if (currentHr in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 21, 22, 23]):
        led.turnOn()
    else:
        led.turnOff()

def humidity(humidity):
    if (humidity > 80):
        humidifier.turnOff()
    else:
        humidifier.turnOn()
'''
