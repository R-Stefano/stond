import sensors, requests, configs, controller, LoggerManager
logger = LoggerManager.logger

class SensorObject():
  def __init__(self, name):
    self.name = name
    self.value = None
    self.isWorking = False


def sendData():
  data = {
    'deviceId': configs.deviceId,
    'sensors': [
      {'name': 'water_temperature', 'value': sensors.water.temperature, 'isWorking': sensors.water.temperatureSensorWorking},
      {'name': 'water_level', 'value': sensors.water.level, 'isWorking': sensors.water.levelSensorWorking},
      {'name': 'water_ph', 'value': sensors.water.ph, 'isWorking': sensors.water.phSensorWorking},
      {'name': 'env_temperature', 'value': sensors.environment.temperature, 'isWorking': sensors.environment.temperatureHumiditySensorWorking},
      {'name': 'env_humidity', 'value': sensors.environment.humidity, 'isWorking': sensors.environment.temperatureHumiditySensorWorking}
    ],
    'actuators': [
      {'name': 'ventilation', 'status': controller.ventilation.status, 'isWorking': controller.ventilation.isWorking},
      {'name': 'LED',         'status': controller.led.status, 'isWorking': controller.led.isWorking},
    ]
  }
  response = requests.put(configs.apiUrl + "/api/devices/" + configs.deviceId + "/status", json = data)
  if (response.status_code != 200):
    logger.error("Impossible processing request. Error {} | {}".format(response.status_code, response.text))


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
      {'name': 'ventilation', 'value': controller.ventilation.speed,      'isWorking': controller.ventilation.isWorking},
      {'name': 'LED',         'value': controller.led.status,             'isWorking': controller.led.isWorking},
  ]

  print('| {0:<20} | {1:<10} | {2:<10} |'.format('name', 'status', 'value'))
  print('-' * 50)

  for sensor in sensorsData:
    print('| {0:<20} | {1:<10} | {2:<10} |'.format(sensor['name'], sensor['isWorking'], sensor['value']))

  for actuator in actuatorsData:
    print('| {0:<20} | {1:<10} | {2:<10} |'.format(actuator['name'], actuator['isWorking'], actuator['value']))
