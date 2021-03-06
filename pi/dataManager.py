import sensors, requests, configs, controller, LoggerManager, base64, os
from datetime import datetime
logger = LoggerManager.logger
buffer = [] # Stores all the requests to send to the server - upcoming or failed for later retry

class SensorObject():
  def __init__(self, name):
    self.name = name
    self.value = None
    self.isWorking = False


def sendData():
  data = {
    'deviceId': configs.deviceId,
    'sensors': [
      {'name': 'water_temperature', 'timestamp': datetime.utcnow().isoformat(), 'value': sensors.water.temperature,       'isWorking': sensors.water.temperatureSensorWorking},
      {'name': 'water_level',       'timestamp': datetime.utcnow().isoformat(), 'value': sensors.water.level,             'isWorking': sensors.water.levelSensorWorking},
      {'name': 'water_ph',          'timestamp': datetime.utcnow().isoformat(), 'value': sensors.water.ph,                'isWorking': sensors.water.phSensorWorking},
      {'name': 'env_temperature',   'timestamp': datetime.utcnow().isoformat(), 'value': sensors.environment.temperature, 'isWorking': sensors.environment.temperatureHumiditySensorWorking},
      {'name': 'env_humidity',      'timestamp': datetime.utcnow().isoformat(), 'value': sensors.environment.humidity,    'isWorking': sensors.environment.temperatureHumiditySensorWorking}
    ],
    'actuators': [
      {'name': 'ventilation', 'status': controller.ventilation.status, 'isWorking': controller.ventilation.isWorking},
      {'name': 'LED',         'status': controller.led.status, 'isWorking': controller.led.isWorking},
    ]
  }
  buffer.append(data)

  requestsCounter = 0
  while (requestsCounter < 5 and len(buffer) > 0):
    data = buffer.pop()
    try:
      requests.put(configs.apiUrl + "/api/devices/" + configs.deviceId + "/status", json = data)
    except Exception as e:
      logger.info("Impossible processing request")
      logger.error(e)
      buffer.append(data)
    requestsCounter += 1

  imageFiles = os.listdir('/home/pi/stond/pi/snapshots/')
  if (len(imageFiles) > 0):
    # check if file in snapshots folder - if so, upload
    with open('/home/pi/stond/pi/snapshots/' + imageFiles[0], "rb") as image_file:
      data = base64.b64encode(image_file.read())
      timestamp = imageFiles[0].split(".")[0]
      print(timestamp)      
      response = requests.post(configs.apiUrl + "/api/devices/" + configs.deviceId + "/snapshot", json = {
        "timestamp": timestamp,
        "base64": data
      })
      if (response.status_code != 200):
        logger.error("Impossible processing request. Error {} | {}".format(response.status_code, response.text))
      else:
        #  delete file if success
        os.remove('/home/pi/stond/pi/snapshots/' + imageFiles[0])

def displayData():
  sensorsData = [
      {'name': 'cpu_temperature', 'value': sensors.system.cpu_temperature, 'isWorking': 1},
      {'name': 'water_temperature', 'value': sensors.water.temperature, 'isWorking': sensors.water.temperatureSensorWorking},
      {'name': 'water_level', 'value': sensors.water.level, 'isWorking': sensors.water.levelSensorWorking},
      {'name': 'water_ph', 'value': sensors.water.ph, 'isWorking': sensors.water.phSensorWorking},
      {'name': 'env_temperature', 'value': sensors.environment.temperature, 'isWorking': sensors.environment.temperatureHumiditySensorWorking},
      {'name': 'env_humidity', 'value': sensors.environment.humidity, 'isWorking': sensors.environment.temperatureHumiditySensorWorking}
  ]

  actuatorsData = [
      {'name': 'ventilation Top',    'value': controller.ventilation.speed_top,      'isWorking': controller.ventilation.isWorking},
      {'name': 'ventilation Bottom', 'value': controller.ventilation.speed_bottom,      'isWorking': controller.ventilation.isWorking},
      {'name': 'LED',         'value': controller.led.status,             'isWorking': controller.led.isWorking},
  ]

  print('| {0:<20} | {1:<10} | {2:<10} |'.format('name', 'status', 'value'))
  print('-' * 50)

  for sensor in sensorsData:
    print('| {0:<20} | {1:<10} | {2:<10} |'.format(sensor['name'], sensor['isWorking'], sensor['value']))

  for actuator in actuatorsData:
    print('| {0:<20} | {1:<10} | {2:<10} |'.format(actuator['name'], actuator['isWorking'], actuator['value']))
