cd $(dirname "$(realpath $0)")

pip3 install virtualenv
source ./env/bin/activate
pip3 install -r requirements.txt

echo "TODO ENABLE I2C"

###TODO
# sudo nano /boot/config.txt
# dtoverlay=w1-gpio
# sudo modprobe w1-gpio
# sudo modprobe w1-therm
#
#
#
#


if grep -Fxq "/home/pi/stond/pi/start.sh" /etc/rc.local
then
    echo "Start Command already in the booter file. Start Routine"
    python3 main.py
else
    echo "Adding Start Command to the booter file & Reboot"
    sudo chmod 777 /etc/rc.local
    sudo sed -i 's/exit 0/\/home\/pi\/stond\/pi\/start.sh\nexit 0/' /etc/rc.local
    sudo reboot
fi

