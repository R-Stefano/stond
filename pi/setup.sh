# On flashing Rpi
# ctrl + shift + x
# enable SSH & add wifi credentials

# After flashed
# git clone https://github.com/R-Stefano/stond.git


cd $(dirname "$(realpath $0)")

echo "[AFRODITE SETUP] Installing Libraries"
pip3 install -r requirements.txt

echo "[AFRODITE SETUP] ENABLE I2C, SPI W1-GPIO"
sudo chmod 777 /boot/config.txt
echo "dtparam=i2c_arm=on" | sudo tee /boot/config.txt -a
echo "dtparam=spi=on" | sudo tee /boot/config.txt -a
echo "dtoverlay=w1-gpio" | sudo tee /boot/config.txt -a
sudo modprobe w1-gpio
sudo modprobe w1-therm

echo "[AFRODITE SETUP] TODO - Add script on startup"
sudo cp afrodite.service /lib/systemd/system/afrodite.service
sudo systemctl enable afrodite.service

# Check is running: 
# - ps -aux | grep python3
# - sudo systemctl status afrodite.service

echo "[AFRODITE SETUP] Restarting to Enable Changes"
sudo reboot