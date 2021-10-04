from datetime import datetime
import logger, sensors
import RPi # allo to call GPIO pins

class FanActuator():
    def __init__(self):
        self.status = "OFF"
        self.working = False
        self.FAN_RELAY_GPIO_PIN = 14
        try:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setup(self.FAN_RELAY_GPIO_PIN, RPi.GPIO.OUT)
            RPi.GPIO.output(self.FAN_RELAY_GPIO_PIN, RPi.GPIO.LOW)
            self.working = True
        except Exception as e:
            logger.add("info", "Fan Actuator not working")
            logger.add("error", e)

    def turnOn(self):
        self.status = "ON"
        RPi.GPIO.output(self.FAN_RELAY_GPIO_PIN, RPi.GPIO.HIGH)
        return

    def turnOff(self):
        self.status = "OFF"
        RPi.GPIO.output(self.FAN_RELAY_GPIO_PIN, RPi.GPIO.LOW)
        return

class LightsActuator():
    def __init__(self):
        self.status = "OFF"
        self.working = False
        self.LED_RELAY_GPIO_PIN = 15
        try:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setup(self.LED_RELAY_GPIO_PIN, RPi.GPIO.OUT)
            RPi.GPIO.output(self.LED_RELAY_GPIO_PIN, RPi.GPIO.LOW)
            self.working = True
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

fan = FanActuator()
led = LightsActuator()


def air(temperature):
    if (sensors.environment.working and temperature > 25):
        fan.turnOn()
        return

    if (sensors.environment.working and temperature < 24):
        fan.turnOff()
        return

    if (not sensors.environment.working and datetime.now().minute in [15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35, 55, 56, 57, 58, 59]):
        fan.turnOn()
    else:
        fan.turnOn()

def lights():
    currentHr = datetime.utcnow().hour #UTC TIMEZONE
    if (currentHr in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 21, 22, 23]):
        led.turnOn()
    else:
        led.turnOff()
