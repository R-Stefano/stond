import time, os, configs
from datetime import datetime
import sensors, logger, controller

if not configs.debug:
  os.system("sudo modprobe w1-gpio")

'''
configs = {
  "max_humidity": 90,
  "min_humidity": 70,
}
'''

systemState = {
  "bme280_working": sensors.environment.working,
  "water_temp_working": sensors.water.temperatureSensorWorking,
  "relay_working": False
}


def run():
  # Update measurements
  timestamp = datetime.now()
  sensors.water.cpu
  cpu_temperature = sensors.cpu.temperature
  water_temperature = sensors.water.temperature
  water_level = sensors.water.level # Output 1 if water touch the sensor
  env_temp, env_humidity = sensors.environment.readTempHumidity()

  logger.update('timestamp', timestamp.isoformat())
  logger.update('cpu_temperature', cpu_temperature)
  logger.update('env_temperature', env_temp)
  logger.update('env_humidity', env_humidity)
  logger.update('water_temperature', water_temperature)
  logger.update('water_level', water_level)
  
  #Control
  controller.air(env_temp)
  controller.lights()
  controller.humidity(env_humidity)
  logger.update('fan', controller.fan.status)
  logger.update('led', controller.led.status)
  logger.update('humidifier', controller.humidifier.status)
  print(logger.data)

  #Save
  if (timestamp.second == 0):
    logger.save()

  #END SCRIPT
  

def start():
  while True:
    timestamp = datetime.now()

    if (timestamp.second % configs.snapshotInterval == 0):
      run()
      time.sleep(1)

if __name__ == '__main__':
  start()
