cd $(dirname "$(realpath $0)")

echo "[AFRODITE SETUP] Installing Libraries"
pip3 install virtualenv
source ./env/bin/activate
pip3 install -r requirements.txt

echo "[AFRODITE SETUP] TODO ENABLE SSH"

echo "[AFRODITE SETUP] ENABLE I2C, SPI W1-GPIO"
'''
sudo chmod 777 /boot/config.txt
echo "dtparam=i2c_arm=on" | sudo tee /boot/config.txt -a
echo "dtparam=spi=on" | sudo tee /boot/config.txt -a
echo "dtoverlay=w1-gpio" | sudo tee /boot/config.txt -a

sudo modprobe w1-gpio
sudo modprobe w1-therm
'''

# Adding Start Command to the booter file
# crontab -e 
# @reboot /home/pi/stond/pi/start.sh > /home/pi/cronjob.log &

echo "[AFRODITE SETUP] Restarting to Enable Changes"
sudo reboot