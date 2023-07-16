from flask import Flask, jsonify
import seeed_dht
import smbus
from grove.display.jhd1802 import JHD1802
import threading

app = Flask(__name__)

DEVICE = 0x23  # Default device I2C address

POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value

ONE_TIME_HIGH_RES_MODE_1 = 0x20

bus = smbus.SMBus(1)  # Rev 2 Pi uses I2C bus 1

def convertToNumber(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return result

def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def read_temperature():
    sensor = seeed_dht.DHT("11", 12)
    humidity, temperature = sensor.read()
    if humidity is not None:
        return {
            'humidity': humidity,
            'temperature': temperature
        }
    else:
        return {
            'temperature': temperature
        }

def read_light():
    light_level = readLight()
    return {
        'light_level': light_level
    }

def update_sensor_values():
    while True:
        temperature_data = read_temperature()
        light_data = read_light()

        # Update the global variables holding the sensor values
        global temperature_value
        global light_level_value
        temperature_value = temperature_data
        light_level_value = light_data

        # Display the sensor values on the LCD screen
        display_temperature(temperature_data)
        display_light_level(light_data)

        # Sleep for the specified interval
        time.sleep(temperature_check_interval)

def display_temperature(temperature_data):
    lcd.setCursor(1, 0)
    if 'temperature' in temperature_data:
        temperature = temperature_data['temperature']
        if temperature > 30:
            lcd.write('Temp > 30C   ')
        elif temperature < 10:
            lcd.write('Temp < 10C   ')
        else:
            lcd.write('              ')

def display_light_level(light_data):
    lcd.setCursor(0, 0)
    if 'light_level' in light_data:
        light_level = light_data['light_level']
        lcd.write('Light Level: {:.2f} lx'.format(light_level))
    else:
        lcd.write('              ')

# Grove - 16x2 LCD RGB Backlight connected to I2C port
lcd = JHD1802()
lcd.setCursor(0, 0)
lcd.write('Herby!')

# Global variables to hold the sensor values
temperature_value = {}
light_level_value = {}

temperature_check_interval = 10 * 60  # 10 minutes

# Start a separate thread to update the sensor values
update_thread = threading.Thread(target=update_sensor_values)
update_thread.start()

@app.route('/temperature')
def temperature():
    return jsonify(temperature_value)

@app.route('/light')
def light():
    return jsonify(light_level_value)

if __name__ == '__main__':
    app.run()
