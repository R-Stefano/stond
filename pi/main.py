import time, os, configs
from datetime import datetime
import sensors, logger, controller
import socketManager as socketMng
import dataManager as dataMng

def run():
  # Update measurements
  timestamp = datetime.now()
  print(timestamp)

  cpu_temperature = sensors.cpu.temperature
  sensors.water.getTemperature()
  sensors.water.getLevel() # Output 1 if water touch the sensor
  sensors.water.getPh()
  sensors.environment.readTempHumidity()

  dataMng.displayData()
  logger.update('timestamp', timestamp.isoformat())
  logger.update('cpu_temperature', cpu_temperature)
  
  #Control
  controller.air()
  controller.lights()
  #controller.humidity(env_humidity)

  #Save
  if (timestamp.second == 0):
    dataMng.sendData()

  #END SCRIPT
  

def start():
  socketMng.login()
  
  while True:
    timestamp = datetime.now()

    if (timestamp.second % configs.snapshotInterval == 0):
      run()
      time.sleep(1)

if __name__ == '__main__':
  start()