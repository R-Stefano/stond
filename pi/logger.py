import logging, sys, requests, configs, os
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = os.path.dirname(__file__) + "/system.log"
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

   return logger

def add(level, message):
   if (level == 'info'):
      logger.info(message)
   elif (level == 'error'):
      logger.error(message, exc_info=True)

def update(key, value):
   data[key]=value

def save():
   add('info', 'Send Data')
   response = requests.post(configs.apiUrl + "/api/sensors", data = data)
   if (response.status_code != 200):
      add('error', "Impossible processing request. Error {} | {}".format(response.status_code, response.text))
   clear()

def clear():
   data = {}

logger = logging.getLogger(LOG_FILE)
logger.setLevel(logging.DEBUG) # better to have too much log than not enough
logger.addHandler(get_console_handler())
logger.addHandler(get_file_handler())
# with this pattern, it's rarely necessary to propagate the error up to parent
logger.propagate = False