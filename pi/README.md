# GET STARTED - PROJECT SETUP
inside pi/
```
./setup.sh
source env/bin/activate
python3 main.py setup     #setup config file and ask dev to calibrate ph sensor
```

# DEVELOPMENT
```
source env/bin/activate # to load the required libraries
```

## testing - laptop
python3 -m unittest tests/test_main.py - to run tests suite (on web)

TODO:
- how to run only one test?

## testing - microcontroller
- `python3 main.py`                   - run the main routine
- `python3 main.py sensors`           - snapshot of all sensors current state and readings
- `python3 main.py fan1:off`          - manually turn FAN1 off. Fans available: fan1, fan2. Replace off with low,medium or high to control fan speed. 
- `python3 main.py led:on`            - manually turn LED on. replace off with on to turn it off
- `python3 main.py hum:on`            - manually turn Humidifier on. replace off with on to turn it off
- `python3 main.py hvac:on:heater`    - manually turn HVAC heater mode on. replace off with on to turn it off
- `python3 main.py hvac:on:cooler`    - manually turn HVAC cooler mode on. replace off with on to turn it off


# DEPLOY - On new microcontroller
1. ./setup.sh           - setup pins, install libraries
2. ./deploy.sh          - setup config.ini and ask user to calibrate ph sensor, add script on startup (afrodite.service) and reboots