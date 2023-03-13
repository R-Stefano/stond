import sensors, requests, controller, LoggerManager, base64, os
from datetime import datetime
logger = LoggerManager.logger
readingsQueue = [] # Stores all the requests to send to the server - upcoming or failed for later retry
import main

components = [
  {"type": 'actuator', "name": 'led',                 "actuatorKey": "led",         "isWorkingKey": "isWorking",                      "statusKey": "status",                           "valueKey": "status"},
  {"type": 'actuator', "name": 'humidifier',          "actuatorKey": "humidifier",  "isWorkingKey": "isWorking",                      "statusKey": "status",                           "valueKey": "status"},
  {"type": 'actuator', "name": 'hvac',                "actuatorKey": "hvac",        "isWorkingKey": "isWorking",                      "statusKey": "status",                           "valueKey": "mode"},
  {"type": 'actuator', "name": 'fan_bottom',          "actuatorKey": "ventilation", "isWorkingKey": "fan1_isWorking",                 "statusKey": "fan1_status",                      "valueKey": "fan1_speed"},
  {"type": 'actuator', "name": 'fan_top',             "actuatorKey": "ventilation", "isWorkingKey": "fan2_isWorking",                 "statusKey": "fan2_status",                      "valueKey": "fan2_speed"},
  {"type": 'sensor',   "name": 'cpu_temperature',     "sensorKey": "system",      "isWorkingKey": "cpuSensorWorking",                 "statusKey": "cpuSensorWorking",                 "valueKey": "cpu_temperature"},
  {"type": 'sensor',   "name": 'camera',              "sensorKey": "system",      "isWorkingKey": "cameraWorking",                    "statusKey": "cameraWorking",                    "valueKey": "cameraWorking"},
  {"type": 'sensor',   "name": 'env_temperature',     "sensorKey": "environment", "isWorkingKey": "temperatureHumiditySensorWorking", "statusKey": "temperatureHumiditySensorWorking", "valueKey": "temperature"},
  {"type": 'sensor',   "name": 'env_humidity',        "sensorKey": "environment", "isWorkingKey": "temperatureHumiditySensorWorking", "statusKey": "temperatureHumiditySensorWorking", "valueKey": "humidity"},
  {"type": 'sensor',   "name": 'water_temperature',   "sensorKey": "water",       "isWorkingKey": "temperatureSensorWorking",         "statusKey": "temperatureSensorWorking",         "valueKey": "temperature"},
  {"type": 'sensor',   "name": 'water_level',         "sensorKey": "water",       "isWorkingKey": "levelSensorWorking",               "statusKey": "levelSensorWorking",               "valueKey": "level"},
  {"type": 'sensor',   "name": 'water_ph',            "sensorKey": "water",       "isWorkingKey": "phSensorWorking",                  "statusKey": "phSensorWorking",                  "valueKey": "ph"},
]

class SensorObject():
  def __init__(self, name):
    self.name = name
    self.value = None
    self.isWorking = False

def readComponents():
  '''
    Add data to queue of readings to push to the server
  '''
  for component in components:
    body = {
      "componentName": component['name'],  
      "timestamp": datetime.utcnow().isoformat(),
      "isWorking": None,
      "status": None,
      "value": None,
    }

    if (component['type'] == "sensor"):
      sensorObject = getattr(sensors, component['sensorKey'])
      body["isWorking"] = getattr(sensorObject, component['isWorkingKey'])
      body["status"] = "ON" if getattr(sensorObject, component['statusKey']) == 1 else "OFF"
      body["value"] = getattr(sensorObject, component['valueKey'])
    elif (component['type'] == "actuator"):
      actuatorObject = getattr(controller, component['actuatorKey'])
      body["isWorking"] = getattr(actuatorObject, component['isWorkingKey'])
      body["status"] = getattr(actuatorObject, component['statusKey'])
      body["value"] = getattr(actuatorObject, component['valueKey'])

    #process camera seperatly
    if component['name'] == "camera":
      imageFiles = os.listdir(sensors.system.cameraSnapshotsDirPath)
      if (len(imageFiles) == 0):
        continue # don't send camera reading if no image to upload

      with open(os.path.join(sensors.system.cameraSnapshotsDirPath, imageFiles[0]), "rb") as image_file:
        body["value"] = base64.b64encode(image_file.read()) #load base64 image
        body["timestamp"] = imageFiles[0].split(".")[0]

      #  delete file once processed
      os.remove(os.path.join(sensors.system.cameraSnapshotsDirPath, imageFiles[0]))

    readingsQueue.append(body)

def uploadReadings():
  '''
  push readings to the server
  '''
  print("Readings to upload", len(readingsQueue))
  batchSize = 20
  while len(readingsQueue) > 0:
    batch = readingsQueue[:batchSize]
    print(">> Upload {} readings".format(len(batch)))

    [response, exception] = main.api.uploadSnapshot(main.config.get('main', 'deviceId'), batch)
    
    #if success remove readings from queue, if exception. Try again later
    if (response):
      del readingsQueue[:batchSize]

    if (exception):
      break

    print("Readings queue left", len(readingsQueue))


def displayData(type = 'all'):
  componentsToDisplay = components
  if (type == "sensors"):
    componentsToDisplay = [c for c in components if c['type'] == 'sensor']
  elif (type == "actuators"):
    componentsToDisplay = [c for c in components if c['type'] == 'actuator']

  print()
  print('| {0:<20} | {1:<10} | {2:<10} | {3:<10} |'.format('name', 'isWorking', 'status', 'value'))
  print('-' * 63)
  for component in componentsToDisplay:
    if (component['type'] == "sensor"):
      sensorObject = getattr(sensors, component['sensorKey'])
      print('| {0:<20} | {1:<10} | {2:<10} | {3:<10} |'.format(
        component['name'], 
        getattr(sensorObject, component['isWorkingKey']), 
        "ON" if getattr(sensorObject, component['statusKey']) == 1 else "OFF", 
        getattr(sensorObject, component['valueKey'])
      ))
    elif (component['type'] == "actuator"):
      sensorObject = getattr(controller, component['actuatorKey'])
      print('| {0:<20} | {1:<10} | {2:<10} | {3:<10} |'.format(
        component['name'], 
        getattr(sensorObject, component['isWorkingKey']), 
        getattr(sensorObject, component['statusKey']), 
        getattr(sensorObject, component['valueKey'])
      ))


