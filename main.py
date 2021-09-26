import adafruit_dht
import time, glob, subprocess, os, json, sys, requests
import board
from datetime import datetime
from gpiozero import CPUTemperature

os.system("sudo modprobe w1-gpio")
snapshotInterval = 5
debug = False
apiUrl = "https://stoned-api-f4lrk4qixq-nw.a.run.app"
cpu = CPUTemperature()
configs = {
  "max_humidity": 90,
  "min_humidity": 70,
}

systemState = {
  "bme280_working": False,
  "water_temp_working": False,
  "relay_working": False
}

import smbus2
import bme280
# Setup Humidity and Temp
try:
  port = 1
  address = 0x77
  bus = smbus2.SMBus(port)
  calibration_params = bme280.load_calibration_params(bus, address)
  systemState['bme280_working'] = True
except:
  systemState['bme280_working'] = False

# Setup Water Temp
try:
  base_dir = '/sys/bus/w1/devices/'
  device_folder = glob.glob(base_dir + '28*')[0]
  device_file = device_folder + '/w1_slave'
  systemState['water_temp_working'] = True
except:
  systemState['water_temp_working'] = False

# RELAY
import RPi.GPIO as GPIO # allo to call GPIO pins
try:
  GPIO.setmode(GPIO.BCM)
  FAN_RELAY_GPIO_PIN = 14
  GPIO.setup(FAN_RELAY_GPIO_PIN, GPIO.OUT)
  GPIO.output(FAN_RELAY_GPIO_PIN, GPIO.LOW)

  LED_RELAY_GPIO_PIN = 15
  GPIO.setup(LED_RELAY_GPIO_PIN, GPIO.OUT)
  GPIO.output(LED_RELAY_GPIO_PIN, GPIO.LOW)

  HUMIDIFIER_GPIO_PIN = 17
  GPIO.setup(HUMIDIFIER_GPIO_PIN, GPIO.OUT)
  GPIO.output(HUMIDIFIER_GPIO_PIN, GPIO.LOW)
  systemState['relay_working'] = True
except:
  systemState['relay_working'] = False

snapshotData = {
    "env_humidity": None,
    "env_temperature": None,
    "water_temperature": None,
    "cpu_temperature": None,
    "fan_status": None,
    "light_status": None,
    "humidifier_status": None
}

def readTempHumidity():
  if (systemState['bme280_working']):
    try:
      data = bme280.sample(bus, address, calibration_params)
      snapshotData["env_humidity"] = data.humidity
      snapshotData["env_temperature"] = data.temperature
    except:
      print("Impossible Fetching Temp & Humidity Data")
      return

def manageFan():
  if (systemState['bme280_working']):
    if (snapshotData["env_temperature"] > 25):
      snapshotData["fan_status"] = "ON"
      GPIO.output(FAN_RELAY_GPIO_PIN, GPIO.HIGH)

    if (snapshotData["env_temperature"] < 24):
      snapshotData["fan_status"] = "OFF"
      GPIO.output(FAN_RELAY_GPIO_PIN, GPIO.LOW)

  if (not systemState['bme280_working']):
    if (snapshotData["light_status"] == "ON"):
      if (datetime.now().minute in [15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35, 55, 56, 57, 58, 59]):
        snapshotData["fan_status"] = "ON"
        GPIO.output(FAN_RELAY_GPIO_PIN, GPIO.HIGH)
      else:
        snapshotData["fan_status"] = "OFF"
        GPIO.output(FAN_RELAY_GPIO_PIN, GPIO.LOW)

def manageLED():
  currentHr = datetime.now().hour #UTC TIMEZONE
  if (currentHr in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20, 21, 22, 23]):
    snapshotData["light_status"] = "ON"
    GPIO.output(LED_RELAY_GPIO_PIN, GPIO.HIGH)
  else:
    snapshotData["light_status"] = "OFF"
    GPIO.output(LED_RELAY_GPIO_PIN, GPIO.LOW)

def manageHumidifier():
  if (snapshotData["env_humidity"] > configs["max_humidity"]):
    snapshotData["humidifier_status"] = "OFF"
    GPIO.output(HUMIDIFIER_GPIO_PIN, GPIO.LOW)

  if (snapshotData["env_humidity"] < configs["min_humidity"]):
    snapshotData["humidifier_status"] = "ON"
    GPIO.output(HUMIDIFIER_GPIO_PIN, GPIO.HIGH)

def sendData():
    #print("[{}] Temperature {}°C | Humidity {}% | Water {}°C | CPU {}°C".format(snapshotData["timestamp"].replace("T", " "), snapshotData["env_temperature"], snapshotData["env_humidity"], snapshotData["water_temperature"], snapshotData["cpu_temperature"]))
    print("Send Data")
    response = requests.post(apiUrl + "/api/sensors", data = snapshotData)
    if (response.status_code != 200):
      print("Impossible processing request. Error {} | {}".format(response.status_code, response.text))

def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def readWaterTemp():
  if (systemState['water_temp_working']):
    temp_c = 0
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
    snapshotData["water_temperature"] = temp_c

while True:
  timestamp = datetime.now()

  if (timestamp.second % snapshotInterval == 0):
    # Update measurements
    snapshotData["timestamp"] = datetime.now().isoformat()
    snapshotData["cpu_temperature"] = cpu.temperature

    readWaterTemp()
    readTempHumidity()

    #Control
    manageFan()
    manageLED()
    #manageHumidifier()

    snapshotDataString = ""
    for key in snapshotData:
      snapshotDataString += key + " " + str(snapshotData[key]) + " | "
    print(snapshotDataString)

    systemStateString = ""
    for key in systemState:
      systemStateString += key + " " + str(systemState[key]) + " | "
    print(systemStateString)

  #Save
  if (timestamp.second == 0):
    sendData()

  time.sleep(1)

  #END SCRIPT
