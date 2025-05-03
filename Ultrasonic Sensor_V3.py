import RPi.GPIO as GPIO
import time

US_pin_1_trig = 13# pins for the ultrasonic sensors (trig = trigger)
US_pin_1_echo = 16
US_pin_2_trig = 15
US_pin_2_echo = 18
US_pin_4_trig = 19
US_pin_4_echo = 22
print("... initial pins initialization complete!")

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(US_pin_1_echo, GPIO.IN) # setting ultrasonic echo pins as input
GPIO.setup(US_pin_2_echo, GPIO.IN)
GPIO.setup(US_pin_4_echo, GPIO.IN)

GPIO.setup(US_pin_1_trig, GPIO.OUT) # setting ultrasonic trigger pins as output
GPIO.setup(US_pin_2_trig, GPIO.OUT)
GPIO.setup(US_pin_4_trig, GPIO.OUT)
print ("... GPIO pins' INPUT and OUTPUT identification complete!")

# defining distance threshold
distance_threshold = 35 # in centimeters

# define functions
def get_distance(TRIG, ECHO): # TRIG and ECHO are parameters that will need to be replaced when called
  """Function to calculate the distance of an object that a selected US picks up"""
  # Send a pulse to TRIG
  GPIO.output(TRIG, GPIO.LOW) # ensure TRIG is low initially
  time.sleep(0.1)

  GPIO.output(TRIG, GPIO.HIGH) # send a pulse to TRIG
  time.sleep(0.00001) # 10 microsecond pulse
  GPIO.output(TRIG, GPIO.LOW) # stop the pulse

  start_time = time.time()
  while GPIO.input(ECHO) == 0:
    if time.time() - start_time > 0.05:
      print("Timeout waiting for Echo to start.")
      return None
  start = time.time()

  while GPIO.input(ECHO) == 1:
    if time.time() - start > 0.05:
      print("Timeout waiting for Echo to end.")
      return None
  end = time.time()

  # calculate the time difference
  duration = end - start

  # Calculate the distance (speed of sound is 34300 cm/s)
  distance = duration * 34300 / 2 # divide by 2 because pulse travels to and fro

  return distance

try:
  while True:
    US1_reading = get_distance(US_pin_1_trig, US_pin_1_echo)
    US2_reading = get_distance(US_pin_2_trig, US_pin_2_echo)
    US4_reading = get_distance(US_pin_4_trig, US_pin_4_echo)
    print(f"\tFront US reading: {US1_reading:.2f}")

    if US1_reading < distance_threshold:
      print("Obstacle detected in front of the device")
    print(f"\tRight US reading: {US2_reading:.2f}")

    if US2_reading < distance_threshold:
      print("Obstacle detected on the right of the device")
    print(f"\tLeft US reading: {US4_reading:.2f}") 

    if US4_reading < distance_threshold:
      print("Obstacle detected on the left of the device")
    
    time.sleep(0.2)
except KeyboardInterrupt:
  GPIO.cleanup()
  print("Program has been stopped by user.")