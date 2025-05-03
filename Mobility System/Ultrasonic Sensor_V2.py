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

    start_time = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - start_time > 0.05:
            print("Timeout waiting for Echo to Start")
            return None
    start = time.time()
    
    while GPIO.input(ECHO) == 1:
         if time.time() - start > 0.05:
             print("Timeout waiting for Echo to End")
             return None
    end = time.time()
    
    # Calculate the time difference
    duration = end - start
    
    # Calculate the distance (speed of sound is 34300 cm/s)
    distance = duration * 34300 / 2  # Divide by 2 because pulse travels to and from the object
    
    return distance, duration, end, start
    
'''
    # Wait for the pulse to return to ECHO
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()
'''



try:
    while True:
        distance, duration, end, start = get_distance()
        print(start)
        print(end)
        print(duration)
        time.sleep(1)
        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()  # Clean up GPIO settings when exiting the program

