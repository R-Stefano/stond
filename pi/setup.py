from datetime import datetime
import sensors, controller
import dataManager as dataMng
  

def start():
  print("LEDs Checks")
  controller.led.controlLights(controlLights = "ON")
  resp = input("Lights Should be ON")
  print(resp)
  resp = input("Lights Should be OFF")
  controller.led.controlLights(controlLights = "OFF")
  print(resp)



if __name__ == '__main__':
  start()