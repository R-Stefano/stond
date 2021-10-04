import logging, sys
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "system.log"
data = {}

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger


def update(key, value):
   data[key]=value

def save():
   #print("[{}] Temperature {}°C | Humidity {}% | Water {}°C | CPU {}°C".format(snapshotData["timestamp"].replace("T", " "), snapshotData["env_temperature"], snapshotData["env_humidity"], snapshotData["water_temperature"], snapshotData["cpu_temperature"]))
   print("Send Data")
   response = requests.post(configs.apiUrl + "/api/sensors", data = snapshotData)
   if (response.status_code != 200):
      print("Impossible processing request. Error {} | {}".format(response.status_code, response.text))
   return

def clear():
   data = {}
