
import time, uuid, os
from datetime import datetime
from configparser import ConfigParser
config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))


import sensors, controller, LoggerManager
import socketManager as socketMng
import dataManager as dataMng
import api

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
  #sensors.water.read_ph()
  sensors.water.read_ppm()
  sensors.water.read_temperature()
  sensors.water.read_level() # Output 1 if water touch the sensor
  sensors.environment.readTempHumidity()

  # take a picture every hour
  if (timestamp.minute == 0 and timestamp.second == 0):
    sensors.system.take_picture()
  
  #Control
  controller.ventilation.controlFanSpeed("fan1", 100)
  controller.ventilation.controlFanSpeed("fan2", 100)
  controller.led.controlLights()
  controller.hvac.controlTemperature()
  sensors.water.read_ph(controller.humidifier.controlHumidity())


  dataMng.displayData()
  #Save
  if (timestamp.second == 0):
    dataMng.readComponents()
    dataMng.uploadReadings()

  #END SCRIPT
  print()
  time.sleep(0.2)

def setupDevice(debug=False):
  import statistics as stat
  # RESET CONFIG.INI be sure key params are set to default values
  if(debug):
    config.set('main', 'apiUrl', 'http://localhost:8080')
    config.set('main', 'debug',  "True")
  else:
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
  #m = (4 - 7)/(ph4MeanValue - ph7MeanValue + 0.00000001)
  #b = - (m * ph7MeanValue) - 7
  m = ph7MeanValue
  b = ph4MeanValue
  config.set('ph_sensor', 'param1', str(m))
  config.set('ph_sensor', 'param2', str(b))

  with open('config.ini', 'w') as f:
      config.write(f)

  # register device on server
  [response, exception] = api.registerDevice(deviceId)
  
  if (exception or response.status_code != 200):
      raise "Impossible to register device. More info in system.log"
  print("DEVICE SUBSCRIBED WITH ID\n\n")
  print(deviceId)
  print("\n\n")


def start(_args):
  if (_args.action == "run"):
    while True:
      timestamp = datetime.now()
      if ((timestamp.second % int(config.get('main', 'snapshotInterval'))) == 0):
        routine()

  elif (_args.action == "setup"):
    setupDevice()
  elif (_args.action == "setup:debug"):
    setupDevice(debug=True)
  elif (_args.action == "sensors"):
    sensors.system.read_cpu()
    sensors.water.read_ph()
    sensors.water.read_ppm()
    sensors.water.read_temperature()
    sensors.water.read_level() # Output 1 if water touch the sensor
    sensors.environment.readTempHumidity()
    dataMng.displayData('sensors')
  elif (_args.action == "upload"):
    dataMng.readComponents()
    dataMng.uploadReadings()
  else:
    params = _args.action.split(":")
    actuator = params[0] # fan1, fan2, led, hum, hvac
    state = params[1] # on or off
    mode = params[2] # this currently only for hvac command. expected values: heater or cooler
    if (actuator == "fan1" or actuator == "fan2"):
      _valueMap = {
        "off": 0,
        "low": 33,
        "medium": 66,
        "high": 100 
      }
      while True:
        controller.ventilation.setFanSpeed(actuator, _valueMap[state.lower()])
        time.sleep(1)
    elif (actuator == "led"):
      while True:
        controller.led.controlLights(state.upper())
        time.sleep(1)
    elif (actuator == "hum"):
      while True:
        controller.humidifier.controlHumidity(state.upper())
        time.sleep(1)
    elif (actuator == "hvac"):
      while True:
        controller.hvac.controlTemperature("{}:{}".format(state, mode).upper())
        time.sleep(1)

if __name__ == '__main__':
  try:
    start(args)
  except Exception as e:
    logger.error(e)