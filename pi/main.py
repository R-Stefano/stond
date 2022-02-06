import time, os, configs
from datetime import datetime
import sensors, controller
import socketManager as socketMng
import dataManager as dataMng

def run():
  # Update measurements
  timestamp = datetime.now()
  sensors.system.read_cpu()
  sensors.water.read_ph()
  sensors.water.read_temperature()
  sensors.water.read_level() # Output 1 if water touch the sensor
  sensors.environment.readTempHumidity()

  dataMng.displayData()
  
  #Control
  controller.ventilation.controlFanSpeed()
  controller.led.controlLights()
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
      time.sleep(5)

if __name__ == '__main__':
  start()