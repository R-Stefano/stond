cd $(dirname "$(realpath $0)")

echo "[AFRODITE STARTUP] Installing Libraries"
pip3 install virtualenv
source ./env/bin/activate
pip3 install -r requirements.txt

echo "[AFRODITE STARTUP] TODO ENABLE I2C"

###TODO
# sudo nano /boot/config.txt
# dtoverlay=w1-gpio
# sudo modprobe w1-gpio
# sudo modprobe w1-therm
#
#
#
#


if grep -Fxq "/home/pi/stond/pi/start.sh" ~/.profile
then
    echo "[AFRODITE STARTUP] Start Command already in the booter file. Start Routine"
    python3 /home/pi/stond/pi/main.py
else
    echo "[AFRODITE STARTUP] Adding Start Command to the booter file & Reboot"
    echo "/home/pi/stond/pi/start.sh" >> ~/.profile
    sudo reboot
fi

