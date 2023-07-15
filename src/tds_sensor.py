from gpiozero import MCP3008
import time

# Analog input pin (channel)
ANALOG_PIN = 0

# Calibration factor for converting sensor value to TDS (adjust as needed)
CALIBRATION_FACTOR = 0.5

# Initialize MCP3008 ADC
adc = MCP3008(channel=ANALOG_PIN)

while True:
    try:
        # Read analog value from the sensor
        sensor_value = adc.value

        # Convert analog value to TDS using calibration factor
        tds = sensor_value * CALIBRATION_FACTOR

        # Print the TDS value
        print(f"TDS: {tds:.2f} ppm")

        # Delay before next reading
        time.sleep(1)

    except KeyboardInterrupt:
        break
