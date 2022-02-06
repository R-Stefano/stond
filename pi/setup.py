from datetime import datetime
import sensors, controller
import dataManager as dataMng
  

def start():
  print("LEDs Checks")
  controller.led.controlLights("ON")
  resp = input("Lights Should be ON (Enter to continue)")
  print(resp)
  print(resp == "")
  controller.led.controlLights("OFF")
  resp = input("Lights Should be OFF (Enter to continue)")
  print(resp)
  print(resp == "")
  return



if __name__ == '__main__':
  start()