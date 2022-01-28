cd $(dirname "$(realpath $0)")

pip3 install virtualenv
source ./env/bin/activate
pip3 install -r requirements.txt

echo "TODO ENABLE I2C"

python3 main.py
