cd $(dirname "$(realpath $0)")
source ./env/bin/activate

if grep -Fxq "/home/pi/stond/pi/start.sh" ~/.profile
then
    if ps ax | grep -v grep | grep "python3 main.py" > /dev/null
    then
        echo "[AFRODITE] Routing already running"
    else
        echo "[AFRODITE] Start Command already in the booter file. Start Routine"
        python3 /home/pi/stond/pi/main.py
    fi
else
    echo "[AFRODITE] Adding Start Command to the booter file & Reboot"
    echo "/home/pi/stond/pi/start.sh" >> ~/.profile
    sudo reboot
fi

