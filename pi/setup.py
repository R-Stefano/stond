from datetime import datetime
import sensors, controller
import dataManager as dataMng
  

def start():
  testsFailed = []
  print("LIGHTs Checks")
  controller.led.controlLights("ON")
  resp = input("RELAY LED Should be ON - LIGHTS should be OFF (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": "RELAY LED Should be ON"})
    return

  controller.led.controlLights("OFF")
  resp = input("RELAY Should be OFF - LIGHTS should be ON (Enter to continue)")
  if (resp != ""):
    testsFailed.append({"message": "RELAY LED Should be OFF"})
    return



  return



if __name__ == '__main__':
  start()