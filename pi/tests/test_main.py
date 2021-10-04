import unittest
from unittest.mock import MagicMock, patch

import main
class TestSensors(unittest.TestCase):
    # methods whose names start with the letters test. 
    # This naming convention informs the test runner about which methods represent tests.

    def setUp(self):
        return

    def test_run(self):
        main.run()
        self.assertEqual('foo'.upper(), 'FOO')

    def tearDown(self):
        return

if __name__ == '__main__':
    unittest.main()