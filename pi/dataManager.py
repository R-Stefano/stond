import sensors, requests, configs, controller

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
  #if (response.status_code != 200):
  #  add('error', "Impossible processing request. Error {} | {}".format(response.status_code, response.text)))


def displayData():
  sensorsData = [
      {'name': 'water_temperature', 'value': sensors.water.temperature, 'isWorking': sensors.water.temperatureSensorWorking},
      {'name': 'water_level', 'value': sensors.water.level, 'isWorking': sensors.water.levelSensorWorking},
      {'name': 'water_ph', 'value': sensors.water.ph, 'isWorking': sensors.water.phSensorWorking},
      {'name': 'env_temperature', 'value': sensors.environment.temperature, 'isWorking': sensors.environment.temperatureHumiditySensorWorking},
      {'name': 'env_humidity', 'value': sensors.environment.humidity, 'isWorking': sensors.environment.temperatureHumiditySensorWorking}
  ]

  actuatorsData = [
      {'name': 'ventilation', 'status': controller.ventilation.status, 'speed': controller.ventilation.speed, 'isWorking': controller.ventilation.isWorking},
      {'name': 'LED',         'status': controller.led.status, 'speed': 1, 'isWorking': controller.led.isWorking},
  ]

  print('| {"name":<20} | {"status":<10} | {"value":<10} |'.format(*range(8)))
  print('-' * 50)

  for sensor in sensorsData:
    print(sensor['name'], sensor['isWorking'], sensor['value'])
    print('| {0:<20} | {1:<10} | {2:<10} |'.format(sensor['name'], sensor['isWorking'], sensor['value']))

  for actuator in actuatorsData:
    print('| {0:<20} | {1:<10} | {2:<10} |'.format(actuator['name'], actuator['isWorking'], actuator['status']))
