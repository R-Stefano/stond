import time, os, configs
from datetime import datetime
import sensors, controller, LoggerManager
import socketManager as socketMng
import dataManager as dataMng

logger = LoggerManager.logger

def run():
  print()
  # Update measurements
  timestamp = datetime.now()
  sensors.system.read_cpu()
  sensors.water.read_ph()
  sensors.water.read_temperature()
  sensors.water.read_level() # Output 1 if water touch the sensor
  sensors.environment.readTempHumidity()

  
  #Control
  controller.ventilation.controlFanSpeed()
  controller.led.controlLights()
  #controller.humidity(env_humidity)

  dataMng.displayData()
  #Save
  if (timestamp.second == 0):
    dataMng.sendData()

  #END SCRIPT
  

def start():
  socketMng.login()

  ### Add startup command to /etc/rc.local (if file available and not already there)
  #with open('/etc/rc.local', 'a') as f:
  #  if '/home/pi/stond/pi/start.sh' not in f.read():
  #    f.write('/home/pi/stond/pi/start.sh #Startup main routine on boot')
  
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