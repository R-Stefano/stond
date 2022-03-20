from datetime import datetime
from os import stat
import sensors, controller
import dataManager as dataMng
import time, uuid
import statistics as stat
from configparser import ConfigParser
config = ConfigParser()

def start():
  testsFailed = []
  print("FAN CHECKS")
  '''
  TESTS
  - main fan off
  - main fan default mode
  - main fan max speed
  - service fan on
  - service fan off
  '''
  message = "TOP FAN Should be OFF"
  print(">>" + message)
  controller.ventilation.controlFanSpeed("top", 0)
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return
  
  message = "TOP FAN Should be 25%"
  print(">>" + message)
  controller.ventilation.controlFanSpeed("top", 25)
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  message = "TOP FAN Should be 100%"
  print(">>" + message)
  controller.ventilation.controlFanSpeed("top", 100)
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  message = "BOTTOM FAN Should be OFF"
  print(">>" + message)
  controller.ventilation.controlFanSpeed("bottom", 0)
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return
  
  message = "BOTTOM FAN Should be 25%"
  print(">>" + message)
  controller.ventilation.controlFanSpeed("bottom", 25)
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  message = "BOTTOM FAN Should be 100%"
  print(">>" + message)
  controller.ventilation.controlFanSpeed("bottom", 100)
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  print("LIGHTS CHECKS")
  message = "RELAY LED Should be ON - LIGHTS should be ON"
  print(">>" + message)
  controller.led.controlLights("ON")
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  message = "RELAY LED Should be OFF - LIGHTS should be OFF"
  print(">>" + message)
  controller.led.controlLights("OFF")
  resp = input("## Enter to continue ##")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  ##print("CAMERA CHECKS")
  ##message = "CAMERA SHOULD TAKE IMAGE"
  ##print(">>" + message)
  ##sensors.system.take_picture()
  ##time.sleep(1)

  ##print("EC SENSOR CHECKS")
  ##message = "PH SENSOR Should read 4"
  ##print(">>" + message)
  ##while (True):
  ##  print(sensors.water.read_ppm())
  ##  time.sleep(1)
    
  print("WATER LEVEL CHECKS")
  message = "Water Level Should read 1"
  print(">>" + message)
  print(sensors.water.levelSensorWorking, sensors.water.read_level())

  while (sensors.water.read_level() == 0):
    print(sensors.water.levelSensorWorking, sensors.water.read_level(), end="\r")
    time.sleep(1)

  print("ENV TEMP & HUMIDITY LEVEL CHECKS")
  message = "Env Temp and Humidity should be ok"
  print(">>" + message)
  temp, humidity = sensors.environment.readTempHumidity()
  print(sensors.environment.temperatureHumiditySensorWorking, temp, humidity)
  while (temp == 0 or humidity == 0):
    temp, humidity = sensors.environment.readTempHumidity()
    print(sensors.environment.temperatureHumiditySensorWorking, temp, humidity, end="\r")
    time.sleep(1)
  
  print("PH SENSOR SETUP")
  message = "Immerge PH SENSOR in solution pH 4"
  print(">>" + message)
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

  message = "Immerge PH SENSOR in solution pH 7"
  print(">>" + message)
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

  print("WATER TEMP CHECKS")
  message = "Water Temperature Should be ok"
  print(">>" + message)
  print(sensors.water.temperatureSensorWorking)
  print(sensors.water.temperatureSensorWorking, sensors.water.read_temperature())
  while (sensors.water.read_temperature() == 0):
    print(sensors.environment.temperatureHumiditySensorWorking, sensors.water.read_temperature(), end="\r")
    time.sleep(1)

  print("Generate Device ID")
  deviceId = str(uuid.uuid4())
  print(deviceId)

  config.read('config.ini')
  config.add_section('main')
  config.set('main', 'deviceId', deviceId)

  config.add_section('ph_sensor')
  #Calcuate ph coeff
  m = (4 - 7)/(ph4MeanValue - ph7MeanValue)
  b = - (m * ph7MeanValue) - 7
  print(m, b)
  config.set('ph_sensor', 'param1', str(m))
  config.set('ph_sensor', 'param2', str(b))

  with open('config.ini', 'w') as f:
      config.write(f)

if __name__ == '__main__':
  start()