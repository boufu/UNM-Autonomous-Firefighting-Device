# this is the main code for the firefighting device #

# ===========================================================================================
# python libraries/packages installs and imports
# ===========================================================================================

# installing python libraries (need to install in the RBPi using its bash CLI) 
  # pip install RPi.GPIO
  # pip install gpiozero

# importing libraries - might show yellow squiggly lines below...
# ...because I need to download the packages on the RBPi hardware, not on my own laptop.
import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import Servo # import servo from gpiozero module 
from gpiozero import DistanceSensor # import distance sensor from gpiozero module
import time

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

servo_pin =  # pin for the nozzle's servo motor 

pump_pin =  # pin for the water pump

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

motor_pin_1 = # pins for the motor
motor_pin_2 = 

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

GPIO.setup(motor_pin_1, GPIO.OUT) # setting motor pins as output
GPIO.setup(motor_pin_2, GPIO.OUT)

# ===========================================================================================
# [WIP] Fire Extinguishing (Nozzle & Servo)
# ===========================================================================================
# initialize PWM (pulse-width modulation - PWM turns power on and off quickly; the longer it stays on ON, the higher the power)
servo = GPIO.PWM(servo_pin, 50) # 50 Hz frequency PWM
servo.start(0) # start with a neutral position

# defining functions
def set_servo_angle(angle):
    """Converts an angle to a duty cycle and moves the servo"""
    duty_cycle = 2 + (angle / 18)  # convert angle to duty cycle (approximate)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # give the servo time to move

def extinguishing_activate(sweep_angle = 60, cycles = 3): # sweep_angle = angles to sweep for per cycle; cycles = number of cycles to sweep
  """Turns on pump and sweeps servo motor"""
  try:
    print("Turning on water pump...")
    GPIO.output(pump_pin, GPIO.HIGH)  # turn on pump
    
    for i in range(cycles):
      set_servo_angle(90 + sweep_angle)  # move servo up
      set_servo_angle(90 - sweep_angle)  # move servo down

  except KeyboardInterrupt: # stop function if there's any keyboard input
    pass  # allow stopping with ctrl+c

def extinguishing_stop():
  """Turns off pump and returns servo motor to neutral position"""
  GPIO.output(pump_pin, GPIO.LOW) # turns off water pump
  servo.ChangeDutyCycle(0)  # stop sending PWM signals

# ===========================================================================================
# [WIP] Fire Detection System # need an analog-digital converter if want to read IR value range
# ===========================================================================================
# read IR sensors' value 







# ===========================================================================================
# [WIP] Mobility System 
# ===========================================================================================

distance_threshold = 0.5 # in meters

ultrasonic_1 = DistanceSensor(US_pin_1_echo, US_pin_1_trig) # setting variables ultrasonic_<> as a distance sensor
ultrasonic_2 = DistanceSensor(US_pin_2_echo, US_pin_2_trig)
ultrasonic_3 = DistanceSensor(US_pin_3_echo, US_pin_4_trig)
ultrasonic_4 = DistanceSensor(US_pin_4_echo, US_pin_4_trig)

def mobility_system():
  if ultrasonic_1.distance >= distance_threshold:
    pass # device moves forward #
  elif ultrasonic_2.distance >= distance_threshold:
    pass # device turns left #
  elif ultrasonic_4.distance >= distance_threshold:
    pass # device turns right #
  elif ultrasonic_3.distance >= distance_threshold:
    pass # reverse device #
  else:
    pass # sound an alarm #



