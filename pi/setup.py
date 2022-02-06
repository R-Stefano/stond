from datetime import datetime
import sensors, controller
import dataManager as dataMng
import time

def start():
  testsFailed = []
  print("PH SENSOR CHECKS")
  message = "PH SENSOR Should read 4"
  while (sensors.water.read_ph() < 3.9 or sensors.water.read_ph() > 4.1):
    print(sensors.water.read_ph() < 3.9)
    print(sensors.water.read_ph() > 4.1)
    time.sleep(1)

  message = "PH SENSOR Should read 7"
  while (sensors.water.read_ph() < 6.9 or sensors.water.read_ph() > 7.1):
    print(sensors.water.read_ph())
    time.sleep(1)
    
  print("LIGHTS CHECKS")
  controller.led.controlLights("ON")
  resp = input("RELAY LED Should be ON - LIGHTS should be ON (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": "RELAY LED Should be ON - LIGHTS should be ON"})
    return

  controller.led.controlLights("OFF")
  resp = input("RELAY Should be OFF - LIGHTS should be OFF (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": "RELAY Should be OFF - LIGHTS should be OFF"})
    return


  print("FAN CHECKS")
  '''
  TESTS
  - main fan off
  - main fan default mode
  - main fan max speed
  - service fan on
  - service fan off
  '''
  controller.ventilation.controlFanSpeed(0)
  message = "MAIN FAN Should be OFF"
  resp = input(message + " (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": message})
    return
  
  controller.ventilation.controlFanSpeed(25)
  message = "MAIN FAN Should be 25%"
  resp = input(message + " (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": message})
    return

  controller.ventilation.controlFanSpeed(100)
  message = "MAIN FAN Should be 100%"
  resp = input(message + " (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": message})
    return
  return



if __name__ == '__main__':
  start()