cd $(dirname "$(realpath $0)")

pip3 install virtualenv
source ./env/bin/activate
pip3 install -r requirements.txt

python3 main.py
