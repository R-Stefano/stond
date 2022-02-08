cd $(dirname "$(realpath $0)")

echo "[AFRODITE SETUP] Installing Libraries"
pip3 install virtualenv
source ./env/bin/activate
pip3 install -r requirements.txt

echo "[AFRODITE STARTUP] TODO ENABLE I2C"

###TODO
# ssh, i2c and spi
# sudo nano /boot/config.txt
# dtoverlay=w1-gpio
# sudo modprobe w1-gpio
# sudo modprobe w1-therm

# Adding Start Command to the booter file
# crontab -e
# @reboot /home/pi/stond/pi/start.sh