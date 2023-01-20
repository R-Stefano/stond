cd $(dirname "$(realpath $0)")

source env/bin/activate
python3 main.py setup

echo "[AFRODITE DEPLOY] Add script on startup"
sudo cp afrodite.service /lib/systemd/system/afrodite.service
sudo systemctl enable afrodite.service

echo "[AFRODITE DEPLOY] Restarting to Enable Changes"
sudo reboot


# Check is running: 
# - ps -aux | grep python3
# - sudo systemctl status afrodite.service