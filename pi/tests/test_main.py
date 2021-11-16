import unittest
from unittest.mock import MagicMock, patch
import sys
import configs
sys.modules['RPi'] = MagicMock()
sys.modules['smbus2'] = MagicMock()
sys.modules['bme280'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['glob'] = MagicMock()


configs.apiUrl = 'http://localhost:8080'
configs.debug = True
import main

main.sensors.water.getTemperature = unittest.mock.Mock(name='getTemperature', return_value=None)
main.sensors.water.temperature = 21

main.sensors.water.getLevel = unittest.mock.Mock(name='getLevel', return_value=None)
main.sensors.water.level = 1

main.sensors.water.getPh = unittest.mock.Mock(name='getPh', return_value=None)
main.sensors.water.ph = 6.5

main.sensors.environment.readTempHumidity = unittest.mock.Mock(name='readTempHumidity', return_value=None)
main.sensors.environment.temperature = 25
main.sensors.environment.humidity = 80


class TestSensors(unittest.TestCase):
    # methods whose names start with the letters test. 
    # This naming convention informs the test runner about which methods represent tests.

    def setUp(self):
        return

    def test_run(self):
        main.start()

    def tearDown(self):
        return

if __name__ == '__main__':
    unittest.main()