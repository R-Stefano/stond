if $AFRODITE_IS_RUNNING == "yes"
then
    exit 1
else
    export AFRODITE_IS_RUNNING="yes"
fi

cd $(dirname "$(realpath $0)")
source ./env/bin/activate

if grep -Fxq "/home/pi/stond/pi/start.sh" ~/.profile
then
    echo "[AFRODITE] Start Command already in the booter file. Start Routine"
    python3 /home/pi/stond/pi/main.py
else
    echo "[AFRODITE] Adding Start Command to the booter file & Reboot"
    echo "/home/pi/stond/pi/start.sh" >> ~/.profile
    sudo reboot
fi

