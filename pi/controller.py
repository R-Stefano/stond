from datetime import datetime
import logger, sensors
import RPi.GPIO as GPIO # allo to call GPIO pins

class FanActuator():
    def __init__(self):
        self.status = "OFF"
        self.working = False
        self.FAN_RELAY_GPIO_PIN = 14
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.FAN_RELAY_GPIO_PIN, GPIO.OUT)
            GPIO.output(self.FAN_RELAY_GPIO_PIN, GPIO.LOW)
            self.working = True
        except Exception as e:
            print(e)
            print("FAN Actuator not working")

    def turnOn(self):
        self.status = "ON"
        GPIO.output(self.FAN_RELAY_GPIO_PIN, GPIO.HIGH)
        return

    def turnOff(self):
        self.status = "OFF"
        GPIO.output(self.FAN_RELAY_GPIO_PIN, GPIO.LOW)
        return

class LightsActuator():
    def __init__(self):
        self.status = "OFF"
        self.working = False
        self.LED_RELAY_GPIO_PIN = 15
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.LED_RELAY_GPIO_PIN, GPIO.OUT)
            GPIO.output(self.LED_RELAY_GPIO_PIN, GPIO.LOW)
            self.working = True
        except Exception as e:
            print(e)
            print("Lights Actuator not working")

    def turnOn(self):
        self.status = "ON"
        GPIO.output(self.LED_RELAY_GPIO_PIN, GPIO.HIGH)
        return

    def turnOff(self):
        self.status = "OFF"
        GPIO.output(self.LED_RELAY_GPIO_PIN, GPIO.LOW)
        return

fan = FanActuator()
led = LightsActuator()


def air():
    print(logger.data['env_temperature'])
    print(sensors.bme280.working)
    if (sensors.bme280.working and sensors.bme280.temperature > 25):
        fan.turnOn()
        return

    if (sensors.bme280.working and sensors.bme280.temperature < 24):
        fan.turnOff()
        return

    if (not sensors.bme280.working and datetime.now().minute in [15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35, 55, 56, 57, 58, 59]):
        fan.turnOn()
    else:
        fan.turnOn()

def lights():
    currentHr = datetime.utcnow().hour #UTC TIMEZONE
    if (currentHr in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 21, 22, 23]):
        led.turnOn()
    else:
        led.turnOff()
