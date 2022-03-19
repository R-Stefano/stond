from datetime import datetime
import sensors, controller
import dataManager as dataMng
import time

def start():
  testsFailed = []
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

  print("PH SENSOR CHECKS")
  ##message = "PH SENSOR Should read 4"
  ##print(">>" + message)
  ##while (sensors.water.read_ph() < 3.9 or sensors.water.read_ph() > 4.1):
  ##  print(sensors.water.read_ph())
  ##  time.sleep(1)

  ##message = "PH SENSOR Should read 7"
  ##print(">>" + message)
  ##while (sensors.water.read_ph() < 6.9 or sensors.water.read_ph() > 7.1):
  ##  print(sensors.water.read_ph())
  ##  time.sleep(1)
    
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
  return


if __name__ == '__main__':
  start()