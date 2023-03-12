import unittest
from unittest.mock import MagicMock, patch
import sys
from types import SimpleNamespace

sys.modules['RPi'] = MagicMock()
sys.modules['smbus2'] = MagicMock()
sys.modules['bme280'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['glob'] = MagicMock()
sys.modules['adafruit_bme280'] = MagicMock()
sys.modules['picamera'] = MagicMock()
sys.modules['gpiozero'] = MagicMock()


import main

main.config.set('main', 'apiUrl', 'http://localhost:8080')
main.config.set('main', 'debug', "True")


main.sensors.system.cpu = unittest.mock.Mock(name='cpu', return_value=None)
main.sensors.water.read_temperature = unittest.mock.Mock(name='read_temperature', return_value=None)
main.sensors.water.read_level = unittest.mock.Mock(name='read_level', return_value=None)
main.sensors.water.get_raw_ph = unittest.mock.Mock(name='get_raw_ph', return_value=None)
main.sensors.water.read_ph = unittest.mock.Mock(name='read_ph', return_value=None)

main.sensors.environment.readTempHumidity = unittest.mock.Mock(name='readTempHumidity', return_value=None)

main.sensors.system.cpu.temperature = 99
main.sensors.water.temperature = 21
main.sensors.water.level = 1
main.sensors.water.raw_ph = 4
main.sensors.water.ph = 6.5

main.sensors.environment.humidity = 80
main.sensors.environment.temperature = 25


class Testing(unittest.TestCase):
    # methods whose names start with the letters test. 
    # This naming convention informs the test runner about which methods represent tests.

    def setUp(self):
        return

    '''
    def test_run(self):
        main.routine()

    def test_device_setup(self):
        args = SimpleNamespace(action='setup')
        main.start(args)

    def test_sensors_state(self):
        args = SimpleNamespace(action='sensors')
        main.start(args)

    def test_fan1_state_control(self):
        args = SimpleNamespace(action="fan1:off")
        main.start(args)
        args = SimpleNamespace(action="fan1:low")
        main.start(args)
        args = SimpleNamespace(action="fan1:medium")
        main.start(args)
        args = SimpleNamespace(action="fan1:high")
        main.start(args)

    def test_fan2_state_control(self):
        args = SimpleNamespace(action="fan2:off")
        main.start(args)
        args = SimpleNamespace(action="fan2:low")
        main.start(args)
        args = SimpleNamespace(action="fan2:medium")
        main.start(args)
        args = SimpleNamespace(action="fan2:high")
        main.start(args)

    def test_led_state_control(self):
        args = SimpleNamespace(action="led:on")
        main.start(args)
        args = SimpleNamespace(action="led:off")
        main.start(args)
        
    def test_hum_state_control(self):
        args = SimpleNamespace(action="hum:on")
        main.start(args)
        args = SimpleNamespace(action="hum:off")
        main.start(args)

    def test_hvac_heater_state_on(self):
        args = SimpleNamespace(action="hvac:on:heater")
        main.start(args)

    def test_hvac_heater_state_on(self):
        args = SimpleNamespace(action="hvac:off:heater")
        main.start(args)

    def test_hvac_cooler_state_on(self):
        args = SimpleNamespace(action="hvac:on:cooler")
        main.start(args)
    '''

    def test_hvac_cooler_state_off(self):
        args = SimpleNamespace(action="hvac:off:cooler")
        main.start(args)

    def tearDown(self):
        return
if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as e:
        main.config.set('main', 'apiUrl', 'https://stoned-api-f4lrk4qixq-nw.a.run.app')
        main.config.set('main', 'debug', "False")