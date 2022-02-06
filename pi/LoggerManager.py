import logging, sys, requests, configs, os
from logging.handlers import TimedRotatingFileHandler
import socketManager as socketMng

data = {
      'deviceId': configs.deviceId
}

def get_logger(logger_name):

   return logger

def add(level, message):
   if (level == 'info'):
      logger.info(message)
   elif (level == 'error'):
      logger.error(message, exc_info=True)

def update(key, value):
   data[key]=value

def display():
   for key in data:
      print(key, data[key])

def save():
   add('info', 'Send Data')

   clear()

def clear():
   data = {
      'deviceId': configs.deviceId
   }

# create logger
FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
LOG_FILE = os.path.dirname(__file__) + "/system.log"

logger = logging.getLogger(LOG_FILE)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(FORMATTER) # add formatter to ch
logger.addHandler(ch) # add ch to logger

# Create a new file every day at midnight
file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
file_handler.setFormatter(FORMATTER)
logger.addHandler(file_handler)

# with this pattern, it's rarely necessary to propagate the error up to parent
logger.propagate = False