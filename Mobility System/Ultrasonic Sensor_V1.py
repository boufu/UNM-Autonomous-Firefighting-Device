import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set GPIO pins for the ultrasonic sensor
TRIG = 17
ECHO = 18

# Set the TRIG and ECHO pins as output and input
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure the distance
def get_distance():
    # Send a pulse to TRIG
    GPIO.output(TRIG, GPIO.LOW)  # Ensure TRIG is low initially
    time.sleep(0.1)
    
    GPIO.output(TRIG, GPIO.HIGH)  # Send a pulse to TRIG
    time.sleep(0.00001)           # 10 microsecond pulse
    GPIO.output(TRIG, GPIO.LOW)   # Stop the pulse

    # Wait for the pulse to return to ECHO
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate the time difference
    pulse_duration = pulse_end - pulse_start
    
    # Calculate the distance (speed of sound is 34300 cm/s)
    distance = pulse_duration * 34300 / 2  # Divide by 2 because pulse travels to and from the object
    
    return distance

try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()  # Clean up GPIO settings when exiting the program

