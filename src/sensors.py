import time
import seeed_dht
import smbus
from grove.display.jhd1802 import JHD1802
import RPi.GPIO as GPIO
import os

#### LED screen ####
DEVICE = 0x23  # Default device I2C address
POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value
ONE_TIME_HIGH_RES_MODE_1 = 0x20

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#### Relay #####
#pins
LED_LIGHTS = 22
PUMP_1 = 17
PUMP_2 = 18
VENTILATOR = 27

GPIO.setmode(GPIO.BCM)
relay_pins = [LED_LIGHTS, PUMP_1, PUMP_2, VENTILATOR] 
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)

def control_relay(pin, state):
    GPIO.output(pin, state)    

def check_relay_status():
    current_month = time.localtime().tm_mon
    filename = f"relay_status_{current_month}.txt"

    if os.path.isfile(filename):
        # The file exists, meaning the relay has already been activated this month
        return True
    else:
        # The file doesn't exist, indicating the relay hasn't been activated this month
        # Create the file to mark that the relay has been activated for this month
        with open(filename, 'w'):
            pass
        return False

def convertToNumber(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return result

def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def main():
    lcd = JHD1802()

    lcd.setCursor(0, 0)
    lcd.write('Fuck Herby!')

    # Temperature
    sensor = seeed_dht.DHT("11", 12)
    
    temperature_check_interval = 10 * 60  # 10 minutes
    light_check_interval = 30 * 60  # 30 minutes
    
    next_temperature_check = time.time()
    next_light_check = time.time()

    while True:
    current_time = time.localtime()

        if current_time >= next_temperature_check:
            humi, temp = sensor.read()
            if humi is not None:
                print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
            else:
                print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
                
            if temp < 30:
                control_relay(VENTILATOR, GPIO.LOW) 
            elif temp > 30:
                control_relay(VENTILATOR, GPIO.HIGH) 
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
            
        if current_time.tm_hour >= 9 and current_time.tm_hour < 18:
           control_relay(LED_LIGHTS, GPIO.HIGH) 
           if not check_relay_status():
            # Activate the relay for the current month
            control_relay(PUMP_1, GPIO.HIGH)
            control_relay(PUMP_2, GPIO.HIGH)
            time.sleep(120)  # Wait for 2 minutes (2 mins = 120 seconds)
            control_relay(PUMP_1, GPIO.LOW)  # Turn off the relay
            control_relay(PUMP_2, GPIO.LOW)
        else:
            control_relay(LED_LIGHTS, GPIO.HIGH) 
        
        time.sleep(5) 
        

GPIO.cleanup() #it's ok because of the while True 

if __name__ == '__main__':
    main()
