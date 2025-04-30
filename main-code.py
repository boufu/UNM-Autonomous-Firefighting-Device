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
from gpiozero import Servo # import servo from gpiozero module 
from gpiozero import Angularservo
import time
import spidev # import package to communicate with SPI devices 
import board # import library that gives names to the RB Pi's physical pins
import busio # import library that enables I2C communication
from adafruit_ads1x15.analog_in import Analogin # import the analogin library from adafruit
import adafruit_ads1x15.ads1115 as ADS # give the adafruit library for ads1115 an alias called ADS

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

servo_pin = 33 # pin for the nozzle's servo motor 

pump_pin = 7 # pin for the water pump

IR_pin_1 =  # pins for the infrared sensors
IR_pin_2 = 
IR_pin_3 =
IR_pin_4 = 

US_pin_1_trig = # pins for the ultrasonic sensors (trig = trigger)
US_pin_1_echo =
US_pin_2_trig =
US_pin_2_echo = 
US_pin_3_trig = 
US_pin_3_echo = 
US_pin_4_trig = 
US_pin_4_echo = 

motor_pin_left_PWM = # pins for the motor
motor_pin_left_DIR = 
motor_pin_right_PWM = 
motor_pin_right_DIR = 

print("... initial pins initialization complete!")
# ===========================================================================================
# identifying the GPIO pins as input/output
# ===========================================================================================
print ("GPIO pins' INPUT and OUTPUT identification start...")

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(pump_pin, GPIO.OUT) # setting pump pin as output

GPIO.setup(IR_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(IR_pin_2, GPIO.IN)
GPIO.setup(IR_pin_3, GPIO.IN)
GPIO.setup(IR_pin_4, GPIO.IN)

GPIO.setup(US_pin_1_echo, GPIO.IN) # setting ultrasonic echo pins as input
GPIO.setup(US_pin_2_echo, GPIO.IN)
GPIO.setup(US_pin_3_echo, GPIO.IN)
GPIO.setup(US_pin_4_echo, GPIO.IN)

GPIO.setup(US_pin_1_trig, GPIO.OUT) # setting ultrasonic trigger pins as output
GPIO.setup(US_pin_2_trig, GPIO.OUT)
GPIO.setup(US_pin_3_trig, GPIO.OUT)
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
servo = AngularServo(33, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
servo.angle = 90 # set servo.angle to default position
time.sleep(1)
print("Servo motor initialized on Pin 33 (board).")

# define functions
def servo_start():
  """Function to set the servo motor to control the nozzle and turn on the pump"""
  try:
    print("Pump and servo are enabled!")
    GPIO.output(pump_pin, GPIO.HIGH) # turn on pump
    for i in range(3):
      print(f"\tCurrent servo cycle: {i+1}")
      position = 80
      counter = 0

      while counter < 3:
        position += 20
        servo.angle = position
        time.sleep (0.6)
        counter += 1
      
      counter = 0 
      while counter < 6:
        position -+ 20
        servo.angle = position
        time.sleep(0.6)
        counter += 1
      
      counter = 0 
      while counter < 3:
        position +- 20
        servo.angle = position
        time.sleep(0.6)
        counter += 1
    
    servo.angle = 90
  except KeyboardInterrupt: # stop function if there's any keyboard input
    print("\nProgram stopped by user.")  # allow stopping with ctrl+c

def servo_stop():
  """Turns off pump and returns servo motor to neutral position"""
  print("Pump and servo are disabled!")
  GPIO.output(pump_pin, GPIO.LOW) # turns off water pump
  servo.angle(90)  # set servo (and nozzle) back to default position


# ===========================================================================================
# [WIP - Motor] Mobility System 
# ===========================================================================================
# defining distance threshold
distance_threshold = 35 # in centimeters

# initialize PWM for motor PWM pins
motor_left_PWM = GPIO.PWM(motor_pin_left_PWM, 200) # 200 Hz PWM
motor_right_PWM = GPIO.PWM(motor_pin_right_PWM, 200) # 200 Hz PWM
motor_left_PWM.start(0) # start at neutral position
motor_right_PWM.start(0) # start at neutral position

print("The Motors' PWM has been enabled!")

# define functions
def get_distance(TRIG, ECHO): # TRIG and ECHO are parameters that will need to be replaced when calleds
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
  print("Motors have been disabled!")

def move_forward(speed=70, duration=0.2):
  """Function to move both motors in the forward direction"""
  print("Moving forward.")
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  motor_left_PWM.ChangeDutyCycle(speed) # duty cycle is in terms of percentage
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def move_backward(speed=70, duration=0.2):
  """Function to move both motors in the reverse direction"""
  print("Moving backward.")
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def turn_left(speed=70, duration=0.1):
  """Function to move left motor in the reverse dir. and right motor in the forward dir."""
  print("Turning left.")
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def turn_right(speed=70, duration=0.1):
  """Function to move right motor in the reverse dir. and the left motor in the forward dir."""
print("Turning right.")
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def mobility_system():
  """Basic autonomous navigation of the device"""
  if get_distance(US_pin_1_trig, US_pin_1_echo) >= distance_threshold:
    move_forward # device moves forward #
  elif get_distance(US_pin_4_trig, US_pin_4_echo) >= distance_threshold:
    turn_left # device turns left #
  elif get_distance(US_pin_2_trig, US_pin_2_echo) >= distance_threshold:
    turn_right # device turns right #
  elif get_distance(US_pin_3_trig, US_pin_3_echo) >= distance_threshold:
    move_backward # reverse device #
  else:
    pass # sound an alarm #

# ===========================================================================================
# [WIP] Fire Detection System # need an analog-digital converter if want to read IR value range
# ===========================================================================================

# initializing ir threshold
ir_threshold = 1000 # ir value threshold

# setting up I2C communication
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C communication has been set up.")
# initiate ADS1115
ads = ADS.ADS1115(i2c)
print("ADS1115 has been initialized.")

# set up communication between infrared sensors and the ads1115
ir_sensor_1 = AnalogIn(ads, ADS.P0) # front infrared sensor using pin A0
ir_sensor_2 = AnalogIn(ads, ADS.P1) # back infrared sensor 2 using pin A1
ir_sensor_3 = AnalogIn(ads, ADS.P2) # left infrared sensor 3 using pin A2 
ir_sensor_4 = AnalogIn(ads, ADS.P3) # front infrared sensor 4 using pin A3  
print("Communication between IR sensors and ADS1115 has been set up.")

# create fire detection flag
fire_detected = False # initial flag's state

# define functions
def fire_detection_loop():
  """Read IR sensors and compare against threshold value to detect fire and set off a flag"""
  pass # read the ir sensor's values

  if any( > threshold for ir_sensors in [, , , ]): # for all sensos above the threshold, fire_detected flag changes to True, otherwise change to False
    fire_detected = True
  else:
    fire_detected = False

def fire_extinguishing_start():
  """Function that starts the fire extinguishing part"""
  ir_sensor_array = [ir_sensor_1, ir_sensor_2, ir_sensor_3, ir_sensor_4]
  ir_sensor_array_sorted = sorted(ir_sensor_array, reverse = True)

  if ir_sensor_2 == ir_sensor_array_sorted[0]:
    ir_check = False # set a flag called ir_check to break while loop when condition is fulfilled

    while ir_check == False:
      old_ir_sensor_1 = ir_sensor_1
      turn_right()
      pass # read new ir values 
      if ir_sensor_1 > old_ir_sensor_1:
        pass # skip
      else:
        ir_check = True
    
    ir_check = False

    while ir_check == False:
      old_ir_sensor_1 = ir_sensor_1
      turn_left(duration = 0.02)
      pass # read new ir values
      if ir_sensor_1 > old_ir_sensor_1:
        pass # skip
      else:
        ir_check = True

    ir_check = False

    while ir_check == False:
      old_ir_sensor_1 = ir_sensor_1
      servo_start()
      time.sleep(0.3)
      servo_stop()
      pass # read new ir values
      if ir_sensor_1 >= ir_threshold:
        pass # skip
      else:
        ir_check = True

  else:
    ir_check = False # set a flag called ir_check to break while loop when condition is fulfilled

    while ir_check == False:
      old_ir_sensor_1 = ir_sensor_1
      turn_left()
      pass # read new ir values 
      if ir_sensor_1 > old_ir_sensor_1:
        pass # skip
      else:
        ir_check = True

    ir_check = False

    while ir_check == False:
      old_ir_sensor_1 = ir_sensor_1
      turn_right(duration = 0.02)
      pass # read new ir values
      if ir_sensor_1 > old_ir_sensor_1:
        pass # skip
      else:
        ir_check = True

    ir_check = False

    while ir_check == False:
      old_ir_sensor_1 = ir_sensor_1
      servo_start()
      time.sleep(0.3)
      servo_stop()
      pass # read new ir values
      if ir_sensor_1 >= ir_threshold:
        pass # skip
      else:
        ir_check = True 

# ===========================================================================================
# [WIP] Main Loop
# ===========================================================================================

try:
  while True:
    if fire_detected == False: # if fire is not detected
      mobility_system() # mobility system starts
      fire_detection_loop() # and fire detection follows suit
    elif fire_detected == True: # however, the moment a fire is detected
      while fire_detected == True: # while the fire_detected flag is True
        fire_extinguishing_start() # the extinguishment will happen
        fire_detection_loop() # and the fire detection will follow suit
      servo_stop() # when the fire_detected flag turns False, while loop breaks and extinguishment stops 
except KeyboardInterrupt:
  print("\nProgram stopped by user.")

