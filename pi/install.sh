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

echo "TODO Add start script to booter"

python3 main.py
