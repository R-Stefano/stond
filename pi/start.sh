if grep -Fxq "/home/pi/stond/pi/start.sh" ~/.profile
then
    echo "[AFRODITE STARTUP] Start Command already in the booter file. Start Routine"
    python3 /home/pi/stond/pi/main.py
else
    echo "[AFRODITE STARTUP] Adding Start Command to the booter file & Reboot"
    echo "/home/pi/stond/pi/start.sh" >> ~/.profile
    sudo reboot
fi

