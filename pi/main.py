
import time, uuid
from datetime import datetime
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

import sensors, controller, LoggerManager
import socketManager as socketMng
import dataManager as dataMng

logger = LoggerManager.logger 

import argparse
parser = argparse.ArgumentParser(description = 'Tests')
parser.add_argument('action', type=str, help='The action to execute: sensors, led:on, hvac:off, hum:on', default="run", nargs='?')  
args = parser.parse_args()

def routine():
  #socketMng.login()
  # Update measurements
  timestamp = datetime.now()
  sensors.system.read_cpu()
  sensors.water.read_ph()
  sensors.water.read_ppm()
  sensors.water.read_temperature()
  sensors.water.read_level() # Output 1 if water touch the sensor
  sensors.environment.readTempHumidity()

  # take a picture every hour
  if (timestamp.minute == 0 and timestamp.second == 0):
    sensors.system.take_picture()
  
  #Control
  controller.ventilation.controlFanSpeed("fan2")
  controller.led.controlLights()
  controller.hvac.controlTemperature()
  controller.humidifier.controlHumidity()


  dataMng.displayData()
  #Save
  if (timestamp.second == 0):
    dataMng.sendData()

  #END SCRIPT
  print()
  time.sleep(0.2)

def setupDevice():
  import statistics as stat
  # RESET CONFIG.INI be sure key params are set to default values
  config.set('main', 'apiUrl', 'https://stoned-api-f4lrk4qixq-nw.a.run.app')
  config.set('main', 'debug', "False")

  deviceId = str(uuid.uuid4())
  config.set('main', 'deviceId', deviceId)

  print(">> Immerge PH SENSOR in solution pH 4")
  input(">> Press ENTER when done")
  ph4Values = []
  ph4MeanValue = 999
  ph4StdValue = 999

  while (len(ph4Values) < 50 or ph4StdValue > 5):
      sensors.water.read_ph()
      ph4Values.append(sensors.water.raw_ph)
      if (len(ph4Values) > 5):
        ph4MeanValue = stat.mean(ph4Values[-5:])
        ph4StdValue = stat.stdev(ph4Values[-5:])
        print('>> Reading #{}  {:.2f} | avg {:.2f} | std {:.2f}'.format(len(ph4Values), sensors.water.raw_ph, ph4MeanValue, ph4StdValue), end="\r")

      time.sleep(1)
  print()
  print(">> Value for pH 4 is {}".format(ph4MeanValue))

  print(">> Immerge PH SENSOR in solution pH 7")
  input(">> Press ENTER when done")
  ph7Values = []
  ph7MeanValue = 999
  ph7StdValue = 999

  while (len(ph7Values) < 50 or ph7StdValue > 5):
    sensors.water.read_ph()
    ph7Values.append(sensors.water.raw_ph)
    if (len(ph7Values) > 5):
      ph7MeanValue = stat.mean(ph7Values[-5:])
      ph7StdValue = stat.stdev(ph7Values[-5:])
      print('>> Reading #{}  {:.2f} | avg {:.2f} | std {:.2f}'.format(len(ph7Values), sensors.water.raw_ph, ph7MeanValue, ph7StdValue), end="\r")

    time.sleep(1)
  print()
  print(">> Value for pH 7 is {}".format(ph7MeanValue))

  #Calcuate ph coeff
  m = (4 - 7)/(ph4MeanValue - ph7MeanValue)
  b = - (m * ph7MeanValue) - 7
  m = 3
  b = 7
  config.set('ph_sensor', 'param1', str(m))
  config.set('ph_sensor', 'param2', str(b))

  with open('config.ini', 'w') as f:
      config.write(f)

def start(_args):
  if (_args.action == "run"):
    while True:
      timestamp = datetime.now()

      if ((timestamp.second % int(config.get('main', 'snapshotInterval'))) == 0):
        routine()

  elif (_args.action == "setup"):
    setupDevice()
  elif (_args.action == "sensors"):
    sensors.system.read_cpu()
    sensors.water.read_ph()
    sensors.water.read_ppm()
    sensors.water.read_temperature()
    sensors.water.read_level() # Output 1 if water touch the sensor
    sensors.environment.readTempHumidity()
    dataMng.displaySensorData()
  else:
    params = _args.action.split(":")
    actuator = params[0]
    state = params[1]
    if (actuator == "fan1" or actuator == "fan2"):
      _valueMap = {
        "off": 0,
        "low": 33,
        "medium": 66,
        "high": 100 
      }
      controller.ventilation.setFanSpeed(actuator, _valueMap[state.lower()])
    elif (actuator == "led"):
      controller.led.controlLights(state.upper())
    elif (actuator == "hum"):
      controller.humidifier.controlHumidity(state.upper())
    elif (actuator == "hvac"):
      controller.hvac.controlTemperature(state.upper())

if __name__ == '__main__':
  try:
    start(args)
  except Exception as e:
    logger.error(e)