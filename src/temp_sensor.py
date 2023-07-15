import time
from w1thermsensor import W1ThermSensor

# Create an instance of the DS18B20 temperature sensor
sensor = W1ThermSensor()

def read_temperature():
    # Read the temperature from the DS18B20 sensor
    temperature = sensor.get_temperature()
    return temperature

def main():
    print("Detecting Temperature...")

    while True:
        temperature_value = read_temperature()
        print(f"Temperature: {temperature_value:.2f}°C")
        time.sleep(1)

if __name__ == '__main__':
    main()
