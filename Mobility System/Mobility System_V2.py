import RPi.GPIO as GPIO
import time

US_pin_1_trig = 13# pins for the ultrasonic sensors (trig = trigger)
US_pin_1_echo = 16
US_pin_2_trig = 15
US_pin_2_echo = 18
US_pin_4_trig = 19
US_pin_4_echo = 22

motor_pin_left_PWM = 33 # pins for the motor
motor_pin_left_DIR = 29
motor_pin_right_PWM = 35
motor_pin_right_DIR = 31
print("... initial pins initialization complete!")
time.sleep(1)


GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(US_pin_1_echo, GPIO.IN) # setting ultrasonic echo pins as input
GPIO.setup(US_pin_2_echo, GPIO.IN)
GPIO.setup(US_pin_4_echo, GPIO.IN)

GPIO.setup(US_pin_1_trig, GPIO.OUT) # setting ultrasonic trigger pins as output
GPIO.setup(US_pin_2_trig, GPIO.OUT)
GPIO.setup(US_pin_4_trig, GPIO.OUT)

GPIO.setup(motor_pin_left_PWM, GPIO.OUT) # setting motor pins PWM and DIR as output
GPIO.setup(motor_pin_left_DIR, GPIO.OUT)
GPIO.setup(motor_pin_right_PWM, GPIO.OUT)
GPIO.setup(motor_pin_right_DIR, GPIO.OUT)
print ("... GPIO pins' INPUT and OUTPUT identification complete!")
time.sleep(1)

# defining distance threshold
front_threshold = 40 # in centimeters
front_threshold_during_turn = 50
side_threshold = 40

# initialize PWM for motor PWM pins
motor_left_PWM = GPIO.PWM(motor_pin_left_PWM, 200) # 200 Hz PWM
motor_right_PWM = GPIO.PWM(motor_pin_right_PWM, 200) # 200 Hz PWM
motor_left_PWM.start(0) # start at neutral position
motor_right_PWM.start(0) # start at neutral position
print("The Motors' PWM has been enabled!")
time.sleep(2)

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

def stop_motors():
    """Function to stop motors"""
    motor_left_PWM.ChangeDutyCycle(0)
    motor_right_PWM.ChangeDutyCycle(0)
    print("Both motors have been disabled!")

def move_forward(speed=4, duration=0.8):
    """Function to move both motors in the forward direction"""
    print("Moving forward.")
    motor_left_PWM.ChangeDutyCycle(speed)
    motor_right_PWM.ChangeDutyCycle(speed)
    GPIO.output(motor_pin_left_DIR, GPIO.LOW)
    GPIO.output(motor_pin_right_DIR, GPIO.LOW)
    time.sleep(duration)
    stop_motors()

def move_backward(speed=3, duration=2):
    """Function to move both motors in the reverse direction"""
    print("Moving backward.")
    motor_left_PWM.ChangeDutyCycle(speed)
    motor_right_PWM.ChangeDutyCycle(speed)         
    GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
    GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
    time.sleep(duration)
    stop_motors()
  
def turn_left(speed=9, duration=0.7):
  """Function to slightly turn left"""
  print("Turn left slightly.")
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)         
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  time.sleep(duration)
  stop_motors()
  
def turn_right(speed=9, duration=0.7):
  """Function to slightly turn right"""
  print("Turn right slightly.")
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)         
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  time.sleep(duration)
  stop_motors()
    
  
def turn_left_until_clear(speed=9, max_turn_time=10):
    """Turn left until front path is clear or max_turn_time is exceeded."""
    print("Turning left until front is clear...")

    motor_left_PWM.ChangeDutyCycle(speed)
    motor_right_PWM.ChangeDutyCycle(speed)
    GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
    GPIO.output(motor_pin_right_DIR, GPIO.LOW)

    start_time = time.time() 

    while True:  
        front = get_distance(US_pin_1_trig, US_pin_1_echo)

        if front is not None and front >= front_threshold_during_turn:
            print(f"Front is clear: {front:.2f} cm")
            break

        if time.time() - start_time > max_turn_time:
            print("Max turn time reached — breaking loop.")
            break

    time.sleep(3)
    stop_motors()  
  
def turn_right_until_clear(speed=9, max_turn_time=10):
    """Turn right until front path is clear or max_turn_time is exceeded."""
    print("Turning right until front is clear...")

    motor_left_PWM.ChangeDutyCycle(speed)
    motor_right_PWM.ChangeDutyCycle(speed)
    GPIO.output(motor_pin_left_DIR, GPIO.LOW)
    GPIO.output(motor_pin_right_DIR, GPIO.HIGH)

    start_time = time.time() 

    while True: 
        front = get_distance(US_pin_1_trig, US_pin_1_echo)

        if front is not None and front >= front_threshold_during_turn:
            print(f"Front is clear: {front:.2f} cm")
            break

        if time.time() - start_time > max_turn_time:
            print("Max turn time reached — breaking loop.")
            break

    time.sleep(3)
    stop_motors()  # Changed: moved stop_motors here so it only stops *after* loop ends

def print_distance():
  """Prints the calculated distance of each ultrasonic sensor"""
  # find the distance of obstacles at each ultrasonic sensor
  US1_reading = get_distance(US_pin_1_trig, US_pin_1_echo)
  US2_reading = get_distance(US_pin_2_trig, US_pin_2_echo)
  US4_reading = get_distance(US_pin_4_trig, US_pin_4_echo)
  
  print("Readings Below:")
  
  # print ultrasonic sensors distance results
  if US1_reading is not None:
    print(f"\tFront ultrasonic sensor reading: {US1_reading:.2f}")
  else:
    print("Front ultrasonic sensor reading: No response")
  
  if US2_reading is not None:
    print(f"\tRight ultrasonic sensor reading: {US2_reading:.2f}")
  else:
    print("Right ultrasonic sensor reading: No response")
    
  if US4_reading is not None:
    print(f"\tLeft ultrasonic sensor reading: {US4_reading:.2f}")
  else:
    print("Left ultrasonic sensor reading: No response")
    
  # print warning text if obstacle is less than the distance threshold and inform which side it is at.
  if US1_reading < front_threshold:
    print("WARNING: Obstacle detected in front of the device")
  else:
    pass
    
  if US2_reading < side_threshold:
    print("WARNING: Obstacle detected on the right of the device")
  else:
    pass
    
  if US4_reading < side_threshold:
    print("WARNING: Obstacle detected on the left of the device")
  else:
    pass      

  return US1_reading, US2_reading, US4_reading

def mobility_system():
    """Basic autonomous navigation logic"""

    US1_reading, US2_reading, US4_reading = print_distance()

    if US1_reading is not None and US1_reading >= front_threshold:
        time.sleep(0.1)
        move_forward()  
        
        if US4_reading <= 120: # if left wall is within 1.2 m
          
          if US4_reading < side_threshold - 5:
            print("Left wall is too close.")
            turn_right()
          elif US4_reading > side_threshold + 5:
            print("Left wall is too far.")
            turn_left()

      
    elif US1_reading is not None and US1_reading < front_threshold:

      if US2_reading is not None and US4_reading is not None:
        
        if US4_reading >= side_threshold and US2_reading >= side_threshold:
          if US4_reading > US2_reading:
            print("Left wall further than right wall.")
            turn_left_until_clear()
          elif US2_reading > US4_reading:
            print("Right wall further than left wall.")
            turn_right_until_clear()
          elif US2_reading == US4_reading:
            print("Left wall same distance to the right wall.")
            turn_left_until_clear()
            
        elif US4_reading < side_threshold and US2_reading >= side_threshold:
          print("Obstacle detected close on the left!")
          turn_right_until_clear()
        
        elif US2_reading < side_threshold and US4_reading >= side_threshold:
          print("Obstacle detected close on the right!")
          turn_left_until_clear()
        
        else:
          print("Initiating REVERSING algorithm...")
          
          # CHANGED: Move backward a bit before retrying
          move_backward(speed=10, duration=1)

          # Refresh distances after moving back
          US1_reading, US2_reading, US4_reading = print_distance()

          if US4_reading is not None and US4_reading >= side_threshold:
              move_backward(speed=10, duration=1)
              turn_left_until_clear()
          elif US2_reading is not None and US2_reading >= side_threshold:
              move_backward(speed=10, duration=1)
              turn_right_until_clear()
          else:
              print("Still boxed in — trying again.")

# main loop

counter = 1

try:
  while True:
    print(f"\n-------------- Iteration: {counter} --------------")
    mobility_system()
    counter += 1
    time.sleep(1)
  

except KeyboardInterrupt:
  GPIO.cleanup()
  print("Program stopped by user.")
