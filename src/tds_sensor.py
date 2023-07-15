import time
import smbus2

# I2C address of the Grove TDS sensor
TDS_SENSOR_ADDR = 0x0f

# I2C bus number (Raspberry Pi 3A+ uses bus 1)
I2C_BUS = 1

def read_tds():
    with smbus2.SMBus(I2C_BUS) as bus:
        # Read TDS data from the Grove TDS sensor
        data = bus.read_i2c_block_data(TDS_SENSOR_ADDR, 0, 2)
        tds = (data[0] << 8) | data[1]
        return tds

def main():
    print("Detecting TDS...")

    while True:
        tds_value = read_tds()
        print(f"TDS Value: {tds_value:.2f} ppm")
        time.sleep(1)

if __name__ == '__main__':
    main()
