import sensors, requests, controller, LoggerManager, base64, os
from datetime import datetime
logger = LoggerManager.logger
buffer = [] # Stores all the requests to send to the server - upcoming or failed for later retry
import main


def registerDevice(deviceId):
    response = None
    exception = None
    try:
      response = requests.post(main.config.get('main', 'apiUrl') + "/api/devices/", json = {
         "id": deviceId
      })
    except Exception as e:
      logger.error("Impossible Register Device\n{}".format(e))
      exception = e
      
    return (response, exception)

def uploadSnapshot(deviceId, readings):
    response = None
    exception = None
    try:
      response = requests.post(main.config.get('main', 'apiUrl') + "/api/devices/{}/snapshot".format(deviceId), json = {
         "deviceId": deviceId,
         "readings": readings,
      })
    except Exception as e:
      logger.error("Impossible Upload Components Readings\n{}".format(e))
      exception = e
    
    return (response, exception)