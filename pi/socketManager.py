#import, socketio
'''
sio = socketio.Client()
sio.connect(configs.apiUrl)

@sio.on('event')
def on_event(evt):
  print(evt)
  if evt['name'] == 'device/ventilation':
    if evt['data']['value'] == 'on':
      controller.fan.turnOn()
      print(controller.fan.status)
    else:
      controller.fan.turnOff()

  if evt['name'] == 'device/light':
    if evt['data']['value'] == 'on':
      controller.led.turnOn()
    else:
      controller.led.turnOff()

def login():
   sio.emit('login', {'deviceId': configs.deviceId})

def updateAnalytics(data):
   sio.emit('login', data)
  '''
