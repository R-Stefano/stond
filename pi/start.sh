cd $(dirname "$(realpath $0)")
source ./env/bin/activate

if grep -Fxq "/home/pi/stond/pi/start.sh" ~/.profile
then
    if $AFRODITE_IS_RUNNING != "yes"
    then
        echo "[AFRODITE] Start Command already in the booter file. Start Routine"
        python3 /home/pi/stond/pi/main.py
    else
        echo "[AFRODITE] Already Running"
    fi
else
    echo "[AFRODITE] Adding Start Command to the booter file & Reboot"
    echo "/home/pi/stond/pi/start.sh" >> ~/.profile
    sudo reboot
fi

