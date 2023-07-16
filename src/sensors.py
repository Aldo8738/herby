import time
import seeed_dht
import smbus
from grove.display.jhd1802 import JHD1802

DEVICE = 0x23  # Default device I2C address

POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value

# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number. Optional parameter 'decimals'
    # will round to specified number of decimal places.
    result = (data[1] + (256 * data[0])) / 1.2
    return result

def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def main():
    # Grove - 16x2 LCD RGB Backlight connected to I2C port
    lcd = JHD1802()

    lcd.setCursor(0, 0)
    lcd.write('Herby!')

    # Temperature
    sensor = seeed_dht.DHT("11", 12)
    
    temperature_check_interval = 10 * 60  # 10 minutes
    light_check_interval = 30 * 60  # 30 minutes
    
    next_temperature_check = time.time()
    next_light_check = time.time()

    while True:
        current_time = time.time()

        if current_time >= next_temperature_check:
            humi, temp = sensor.read()
            if humi is not None:
                print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
            else:
                print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
                
            if temp > 30:
                lcd.setCursor(1, 0)
                lcd.write('Temp > 30C')
            elif temp < 10:
                lcd.setCursor(1, 0)
                lcd.write('Temp < 10C')
            else:
                lcd.setCursor(1, 0)
                lcd.write('             ')  # Clear the line
            
            next_temperature_check = current_time + temperature_check_interval

        if current_time >= next_light_check:
            lightLevel = readLight()
            print("Light Level: " + format(lightLevel, '.2f') + " lx")
            next_light_check = current_time + light_check_interval

        time.sleep(1)
        # lcd.write(format(lightLevel, '.2f'))


if __name__ == '__main__':
    main()
