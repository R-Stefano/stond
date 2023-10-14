import board

from adafruit_bme280 import basic as adafruit_bme280

address = 0x76

while(1):
    print("[BME280] Reading Temp & Humidity\n")
    try:
        i2c = board.I2C()  # uses board.SCL and board.SDA
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address)
        try:
            humidity = round(bme280.humidity, 2)
            temperature = round(bme280.temperature, 2)
        except Exception as e:
            print("\n[BME280] Impossible Reading Temp & Humidity      ")
            print(e)
            humidity = 0
            temperature = 0
        print("Hum: ")
        print(humidity)
        print(" Temp= ")
        print(temperature)
        print("\n")
    except Exception as e:
        print("\n[BME280] (start) Not working    ")
        print(e)
