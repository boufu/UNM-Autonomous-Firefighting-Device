# this is the main code for the firefighting device #

# ===========================================================================================
# python libraries/packages installs and imports
# ===========================================================================================

# installing python libraries (need to install in the RBPi using its bash CLI)
'''README'''
  # pip install RPi.GPIO
  # pip install gpiozero
  # sudo pip3 install spidev


# importing libraries - might show yellow squiggly lines below...
# ...because I need to download the packages on the RBPi hardware, not on my own laptop.
import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import Servo # import servo from gpiozero module 
from gpiozero import DistanceSensor # import distance sensor from gpiozero module
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
#        4  #         # 2
#           #         #
#           # # # # # #
#                3

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

# ===========================================================================================
# identifying the GPIO pins as input/output
# ===========================================================================================
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(servo_pin, GPIO.OUT) # setting servo pin as output

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

# ===========================================================================================
# Fire Extinguishing (Nozzle & Servo)
# ===========================================================================================
# initialize PWM (pulse-width modulation - PWM turns power on and off quickly; the longer it stays on ON, the higher the power)
servo = GPIO.PWM(servo_pin, 50) # 50 Hz frequency PWM
servo.start(0) # start with a neutral position

# define functions
def set_servo_angle(angle):
    """Converts an angle to a duty cycle and moves the servo"""
    duty_cycle = 2 + (angle / 18)  # convert angle to duty cycle (approximate)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # give the servo time to move

def servo_start(sweep_angle = 60, cycles = 3): # sweep_angle = angles to sweep for per cycle; cycles = number of cycles to sweep
  """Turns on pump and sweeps servo motor"""
  try:
    print("\nTurning on water pump...")
    GPIO.output(pump_pin, GPIO.HIGH)  # turn on pump
    
    for i in range(cycles):
      set_servo_angle(90 + sweep_angle)  # move servo up
      set_servo_angle(90 - sweep_angle)  # move servo down

  except KeyboardInterrupt: # stop function if there's any keyboard input
    pass  # allow stopping with ctrl+c

def servo_stop():
  """Turns off pump and returns servo motor to neutral position"""
  print("\nTurning off water pump...")
  GPIO.output(pump_pin, GPIO.LOW) # turns off water pump
  servo.ChangeDutyCycle(0)  # stop sending PWM signals


# ===========================================================================================
# Mobility System 
# ===========================================================================================
# defining distance threshold
distance_threshold = 0.5 # in meters

# setting variables ultrasonic_<> as a distance sensor
ultrasonic_1 = DistanceSensor(US_pin_1_echo, US_pin_1_trig) 
ultrasonic_2 = DistanceSensor(US_pin_2_echo, US_pin_2_trig)
ultrasonic_3 = DistanceSensor(US_pin_3_echo, US_pin_4_trig)
ultrasonic_4 = DistanceSensor(US_pin_4_echo, US_pin_4_trig)

# initialize PWM for motor PWM pins
motor_left_PWM = GPIO.PWM(motor_pin_left_PWM, 200) # 200 Hz PWM
motor_right_PWM = GPIO.PWM(motor_pin_right_PWM, 200) # 200 Hz PWM
motor_left_PWM.start(0) # start at neutral position
motor_right_PWM.start(0) # start at neutral position

# define functions
def stop_motors():
  """Function to stop motors"""
  motor_left_PWM.ChangeDutyCycle(0)
  motor_right_PWM.ChangeDutyCycle(0)

def move_forward(speed=70, duration=0.2):
  """Function to move both motors in the forward direction"""
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  motor_left_PWM.ChangeDutyCycle(speed) # duty cycle is in terms of percentage
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def move_backward(speed=70, duration=0.2):
  """Function to move both motors in the reverse direction"""
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def turn_left(speed=70, duration=0.1):
  """Function to move left motor in the reverse dir. and right motor in the forward dir."""
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def turn_right(speed=70, duration=0.1):
  """Function to move right motor in the reverse dir. and the left motor in the forward dir."""
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

def mobility_system():
  """Basic autonomous navigation of the device"""
  if ultrasonic_1.distance >= distance_threshold:
    move_forward # device moves forward #
  elif ultrasonic_4.distance >= distance_threshold:
    turn_left # device turns left #
  elif ultrasonic_2.distance >= distance_threshold:
    turn_right # device turns right #
  elif ultrasonic_3.distance >= distance_threshold:
    move_backward # reverse device #
  else:
    pass # sound an alarm #

# ===========================================================================================
# [WIP] Fire Detection System # need an analog-digital converter if want to read IR value range
# ===========================================================================================
# create fire detection flag
fire_detected = False # initial flag's state
ir_threshold = 1000 # ir value threshold

# define functions
def fire_detection_loop():
  """Read IR sensors and compare against threshold value to detect fire and set off a flag"""
  pass # need to do the ADC thingy with spidev first i believe

  pass # read IR sensors

  pass # set condition that changes the fire_detected flag to either True or False
  


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
  print("\nLoop stopped by user.")

