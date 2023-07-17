import RPi.GPIO as GPIO
import time

# Set GPIO mode and relay pin
GPIO.setmode(GPIO.BCM)
relay_pin = 17

# Setup relay pin as output
GPIO.setup(relay_pin, GPIO.OUT)

# Function to control the relay
def control_relay(state):
    GPIO.output(relay_pin, state)

# Example usage: turn on the relay
control_relay(GPIO.HIGH)
time.sleep(5)  # Wait for 5 seconds
control_relay(GPIO.LOW)  # Turn off the relay

# Clean up GPIO
GPIO.cleanup()
