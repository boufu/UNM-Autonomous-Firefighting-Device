### this is the main code for the firefighting device which will run upon booting of the Rasberry Pi ###

# ===========================================================================================
# python libraries/packages installs and imports
# ===========================================================================================

# installing python libraries (need to install in the RBPi using its bash CLI)
  # sudo apt install RPi.GPIO
  # sudo apt install gpiozero
  # sudo apt install adafruit...


# importing libraries - might show yellow squiggly lines below...
# because I need to download the packages on the RBPi hardware, not on my own laptop.
import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import AngularServo
import time
GPIO.cleanup()

# ===========================================================================================
# defining variables (pins in this case)
# ===========================================================================================          
#                1
#           # # # # # # 
#           #         #
#        4  #         #  2
#           #         #
#           # # # # # #
#                3

print("Initial pins initialization start...")

servo_pin = 32 # pin for the nozzle's servo motor 

pump_pin = 36 # pin for the water pump

IR_pin_1 = 21 # pins for the infrared sensors
IR_pin_2 = 24
IR_pin_3 = 26
IR_pin_4 = 23

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
# ===========================================================================================
# identifying the GPIO pins as input/output
# ===========================================================================================
print ("GPIO pins' INPUT and OUTPUT identification start...")

GPIO.setmode(GPIO.BOARD) # Use physical pin numbers 

GPIO.setup(pump_pin, GPIO.OUT) # setting pump pin as output

GPIO.setup(IR_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(IR_pin_2, GPIO.IN)
GPIO.setup(IR_pin_3, GPIO.IN)
GPIO.setup(IR_pin_4, GPIO.IN)

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
# ===========================================================================================
# Fire Extinguishing (Nozzle & Servo)
# ===========================================================================================
# initialize angular servo on pin 33
servo = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo.angle = 90 # set servo.angle to default position
time.sleep(1)
print("Servo motor initialized on Pin 33 (board).")

# define functions

def pump_and_servo_start():
  """Starts pump and servo motor."""
  print("Pump and servo motor start!")
  GPIO.output(pump_pin, GPIO.HIGH) # turn on pump
  for i in range(3):
      position = 80
      counter = 0
      print(f"---------Servo Cycle: {i+1}----------")
                                
      while counter < 2:
        position -= 20
        servo.angle = position
        time.sleep(0.6)
        counter += 1
        print(position)
                                
      counter = 0
      while counter < 2:
        position += 20
        servo.angle = position
        time.sleep(0.6)
        counter += 1
        print(position)

        servo.angle = 90
        time.sleep(0.4)
        
def pump_and_servo_stop():
  """Turn off the pump and servo"""
  print("Pump stopped!")
  servo.angle = 90
  GPIO.output(pump_pin, GPIO.LOW)

# ===========================================================================================
# Mobility System 
# ===========================================================================================
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

def move_forward(speed=4, duration=0.6):
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
  
def turn_left(speed=9, duration=0.9):
  """Function to slightly turn left"""
  print("Turn left slightly.")
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)         
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  time.sleep(duration)
  stop_motors()
  
def turn_right(speed=9, duration=0.9):
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

        US4_reading = get_distance(US_pin_4_trig, US_pin_4_echo) # read new left ultrasonic sensor distance
        
        if US4_reading <= 100: # if left wall is within 1 m
          
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
              move_backward(speed=10, duration=3)
              turn_left_until_clear()
          elif US2_reading is not None and US2_reading >= side_threshold:
              move_backward(speed=10, duration=3)
              turn_right_until_clear()
          else:
              print("Still boxed in — trying again.")

# ===========================================================================================
# Fire Detection System 
# ===========================================================================================

fire_detected = False # fire_detected flag initial state

def turn_left_until_fire_detected(speed=9):
    """Turn left until fire detected in front"""
    print("Turning left until fire is in front...")

    motor_left_PWM.ChangeDutyCycle(speed)
    motor_right_PWM.ChangeDutyCycle(speed)
    GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
    GPIO.output(motor_pin_right_DIR, GPIO.LOW)

    start_time = time.time() 

    while True:  
        IR1_reading = GPIO.input(IR_pin_1)
        print(f"Front IR input is {IR1_reading}")

        if IR1_reading == 0:
            print("Fire is at the front — breaking loop.")
            break

        time.sleep(0.1)
    stop_motors()  

def turn_right_until_fire_detected(speed=9):
    """Turn right until fire detected in front"""
    print("Turning right until fire is in front...")

    motor_left_PWM.ChangeDutyCycle(speed)
    motor_right_PWM.ChangeDutyCycle(speed)
    GPIO.output(motor_pin_left_DIR, GPIO.LOW)
    GPIO.output(motor_pin_right_DIR, GPIO.HIGH)

    start_time = time.time() 

    while True:  
        IR1_reading = GPIO.input(IR_pin_1)
        print(f"Front IR input is {IR1_reading}")

        if IR1_reading == 0:
            print("Fire is at the front — breaking loop.")
            break

        time.sleep(0.1)

    stop_motors()  

def fire_detection_loop():
  """Read IR sensors and compare against threshold value to detect fire and set off a flag"""
  
  global fire_detected
  
  IR1_reading = GPIO.input(IR_pin_1)
  IR2_reading = GPIO.input(IR_pin_2)
  IR3_reading = GPIO.input(IR_pin_3)
  IR4_reading = GPIO.input(IR_pin_4)
  print(f"Front IR input is {IR1_reading}")
  print(f"Right IR input is {IR2_reading}")
  print(f"Rear IR input is {IR3_reading}")
  print(f"Left IR input is {IR4_reading}")

  if IR1_reading == 0 or IR2_reading == 0 or IR3_reading == 0 or IR4_reading == 0 : # for all sensors above the threshold, fire_detected flag changes to True, otherwise change to False
    print("Fire detected -  flag set to true")
    fire_detected = True
  else:
    print("No fire detected -  flag remains false")
    fire_detected = False
  
  return IR1_reading, IR2_reading, IR3_reading, IR4_reading

def fire_extinguishing_start():
  IR1_reading, IR2_reading, IR3_reading, IR4_reading = fire_detection_loop()
  
  if IR1_reading == 0:
    IR_check = False
    while IR_check == False:
      pump_and_servo_start() # start servo and pump
      print("Starting servo and pump")
      IR1_reading = GPIO.input(IR_pin_1)
      print(f"Front IR input is {IR1_reading}")

      if IR1_reading == 1:
        IR_check = True

  elif IR2_reading == 0:
    turn_right_until_fire_detected()
    turn_right()
    IR_check = False
    while IR_check == False:
      pump_and_servo_start() # start servo and pump
      print("Starting servo and pump")
      IR1_reading = GPIO.input(IR_pin_1)
      print(f"Front IR input is {IR1_reading}")

      if IR1_reading == 1:
        IR_check = True
      
  elif IR3_reading == 0:
    turn_right_until_fire_detected()
    turn_left()
    IR_check = False
    while IR_check == False:
      pump_and_servo_start() # start servo and pump
      print("Starting servo and pump")
      IR1_reading = GPIO.input(IR_pin_1)
      print(f"Front IR input is {IR1_reading}")

      if IR1_reading == 1:
        IR_check = True

  elif IR4_reading == 0:
    turn_left_until_fire_detected()
    IR_check = False
    while IR_check == False:
      pump_and_servo_start() # start servo and pump
      print("Starting servo and pump")
      IR1_reading = GPIO.input(IR_pin_1)
      print(f"Front IR input is {IR1_reading}")

      if IR1_reading == 1:
        IR_check = True

  pump_and_servo_stop()
  print("Fire successfully put out.")

# ===========================================================================================
# Main Loop
# ===========================================================================================

counter = 1

try:
  while True:
    print(f"\n-------------- Iteration: {counter} --------------")
    if fire_detected == False: # if fire is not detected
      mobility_system() # mobility system starts
      fire_detection_loop() # and fire detection follows suit
    elif fire_detected == True: # however, the moment a fire is detected
      while fire_detected == True: # while the fire_detected flag is True
        fire_extinguishing_start() # the extinguishment will happen
        fire_detection_loop() # and the fire detection will follow suit
    counter += 1
except KeyboardInterrupt:
  GPIO.cleanup()
  print("\nProgram stopped by user.")

