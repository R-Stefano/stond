SETUP - DEVELOPMENT
1. ./setup.sh
2. run source env/bin/activate
3. python3 main.py setup  - setup config file and ask dev to calibrate ph sensor

DEVELOPMENT
1. run source env/bin/activate - to load the required libraries

Test application on Web
python3 -m unittest tests/test_main.py - to run tests suite (on web)

TODO:
- how to run only one test?

Test application on microcontroller
- python3 main.py         - run the main routine
- python3 main.py sensors - snapshot of all sensors current state and readings
- python3 main.py led:on  - manually turn LED on. replace off with on to turn it off
- python3 main.py hum:on  - manually turn Humidifier on. replace off with on to turn it off
- python3 main.py hvac:on - manually turn HVAC on. replace off with on to turn it off

DEPLOYMENT on new microcontroller
1. ./setup.sh           - setup pins, install libraries
2. ./deploy.sh          - setup config.ini and ask user to calibrate ph sensor, add script on startup (afrodite.service) and reboots