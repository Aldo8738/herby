
import time

from grove.display.jhd1802 import JHD1802

def main():
    # Grove - 16x2 LCD RGB Backlight connected to I2C port
    lcd = JHD1802()

    lcd.setCursor(0, 0)
    lcd.write('fuck hfsdf')

    print('application exiting...')

if __name__ == '__main__':
    main()
