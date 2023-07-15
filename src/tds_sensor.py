from gpiozero import MCP3008
import time

# Analog input pin
ANALOG_PIN = 0

# MCP3008 reference voltage (default: 3.3V)
REFERENCE_VOLTAGE = 3.3

# Calibration factor for converting sensor value to TDS (adjust as needed)
CALIBRATION_FACTOR = 0.5

# Initialize MCP3008 ADC
adc = MCP3008(channel=ANALOG_PIN)

while True:
    # Read analog value from the sensor
    analog_value = adc.value

    # Convert analog value to voltage
    voltage = analog_value * REFERENCE_VOLTAGE

    # Convert voltage to TDS using calibration factor
    tds = voltage * CALIBRATION_FACTOR

    # Print the TDS value
    print(f"TDS: {tds:.2f} ppm")

    # Delay before next reading
    time.sleep(1)
