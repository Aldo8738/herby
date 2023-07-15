import grovepi
import time

# Connect the Grove TDS sensor to the appropriate analog Grove socket
sensor = 0  # Change the socket number (0, 1, 2, or 3) as per the connection

while True:
    try:
        # Read the sensor value
        sensor_value = grovepi.analogRead(sensor)

        # Convert sensor value to TDS using calibration factor (adjust as needed)
        calibration_factor = 0.5
        tds = sensor_value * calibration_factor

        # Print the TDS value
        print(f"TDS: {tds:.2f} ppm")

        # Delay before next reading
        time.sleep(1)

    except KeyboardInterrupt:
        break

    except IOError:
        print("Error: Failed to read sensor data.")
