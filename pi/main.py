import time, glob, os, json, sys, requests, configs
from datetime import datetime
import sensors, logger, controller

if not configs.debug:
  os.system("sudo modprobe w1-gpio")

'''
configs = {
  "max_humidity": 90,
  "min_humidity": 70,
}
'''

systemState = {
  "bme280_working": sensors.environment.working,
  "water_temp_working": sensors.water.temperatureSensorWorking,
  "relay_working": False
}

'''
# RELAY
import RPi.GPIO as GPIO # allo to call GPIO pins
try:
  HUMIDIFIER_GPIO_PIN = 17
  GPIO.setup(HUMIDIFIER_GPIO_PIN, GPIO.OUT)
  GPIO.output(HUMIDIFIER_GPIO_PIN, GPIO.LOW)
  systemState['relay_working'] = True
except:
  systemState['relay_working'] = False

def manageHumidifier():
  if (snapshotData["env_humidity"] > configs["max_humidity"]):
    snapshotData["humidifier_status"] = "OFF"
    GPIO.output(HUMIDIFIER_GPIO_PIN, GPIO.LOW)

  if (snapshotData["env_humidity"] < configs["min_humidity"]):
    snapshotData["humidifier_status"] = "ON"
    GPIO.output(HUMIDIFIER_GPIO_PIN, GPIO.HIGH)
'''



def run():
  # Update measurements
  timestamp = datetime.now().isoformat()
  cpu_temperature = sensors.cpu.temperature
  water_temperature = sensors.water.temperature
  water_level = sensors.water.level # Output 1 if water touch the sensor
  env_temp, env_humidity = sensors.environment.readTempHumidity()

  logger.update('timestamp', timestamp)
  logger.update('cpu_temperature', cpu_temperature)
  logger.update('env_temperature', env_temp)
  logger.update('env_humidity', env_humidity)
  logger.update('water_temperature', water_temperature)
  logger.update('water_level', water_level)
  
  print(logger.data)
  #logger.clear()

  #Control
  #controller.air()
  #controller.lights()
  print()
  '''
  #manageHumidifier()

  if (snapshotData['env_temperature'] > 29):
    snapshotData["env_temperature"] = 29

    snapshotDataString = ""
    for key in snapshotData:
      snapshotDataString += key + " " + str(snapshotData[key]) + " | "
    print(snapshotDataString)

    systemStateString = ""
    for key in systemState:
      systemStateString += key + " " + str(systemState[key]) + " | "
    print(systemStateString)

  #Save
  if (timestamp.second == 0):
    logger.save()
  '''

  #END SCRIPT
  

def start():
  while True:
    timestamp = datetime.now()

    if (timestamp.second % configs.snapshotInterval == 0):
      run()
      time.sleep(1)

if __name__ == '__main__':
  start()
