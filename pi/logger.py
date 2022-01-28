import logging, sys, requests, configs, os
from logging.handlers import TimedRotatingFileHandler
import socketManager as socketMng

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = os.path.dirname(__file__) + "/system.log"
data = {
      'deviceId': configs.deviceId
}

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

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

logger = logging.getLogger(LOG_FILE)
logger.setLevel(logging.DEBUG) # better to have too much log than not enough
logger.addHandler(get_console_handler())
logger.addHandler(get_file_handler())
# with this pattern, it's rarely necessary to propagate the error up to parent
logger.propagate = False