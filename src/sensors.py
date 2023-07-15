import time
import seeed_dht
import smbus
from grove.display.jhd1802 import JHD1802

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def main():
    # Grove - 16x2 LCD RGB Backlight connected to I2C port
    lcd = JHD1802()

    lcd.setCursor(0, 0)
    lcd.write('Herby!')

    # Temperature
    sensor = seeed_dht.DHT("11", 12)
    while True:
        humi, temp = sensor.read()
        if not humi is None:
            print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
        time.sleep(1)
        
        lightLevel=readLight()
        print("Light Level : " + format(lightLevel,'.2f') + " lx")
        time.sleep(0.5)
        
        lcd.write(format(lightLevel,'.2f'));
        

if __name__ == '__main__':
    main()