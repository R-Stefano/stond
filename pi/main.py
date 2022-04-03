import time, os, configs
from datetime import datetime
import sensors, controller, LoggerManager
import socketManager as socketMng
import dataManager as dataMng
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

logger = LoggerManager.logger

def run():
  try:
    print(config.get('main', 'deviceId'))
  except Exception as e:
    print("Device ID not found")

  print()
  # Update measurements
  timestamp = datetime.now()
  sensors.system.read_cpu()
  sensors.water.read_ph()
  sensors.water.read_ppm()
  sensors.water.read_temperature()
  sensors.water.read_level() # Output 1 if water touch the sensor
  sensors.environment.readTempHumidity()

  #sensors.system.take_picture()
  
  #Control
  controller.ventilation.controlFanSpeed("top")
  controller.led.controlLights()
  #controller.humidity(env_humidity)

  dataMng.displayData()
  #Save
  if (timestamp.second == 0):
    dataMng.sendData()

  #END SCRIPT
  

def start():
  #socketMng.login()
  
  while True:
    timestamp = datetime.now()

    if ((timestamp.second % configs.snapshotInterval) == 0):
      run()
      time.sleep(0.2)

if __name__ == '__main__':
  try:
    start()
  except Exception as e:
    logger.error(e)