# this is the main code for the firefighting device #

# installing python libraries (need to install in the RBPi using its bash CLI) 
  # pip install RPi.GPIO

# importing libraries - might show yellow squiggly lines below...
# ...because I need to download the packages on the RBPi hardware not on my own laptop.
import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import Servo # import servo from gpiozero module 
from gpiozero import DistanceSensor # import distance sensor from gpiozero module
import time

# initializing pins (signal pins)
ultrasonic_pin_1_trig = 7  
ultrasonic_pin_1_echo = 8 
ultrasonic_pin_2_trig = 10
ultrasonic_pin_2_echo = 11
ultrasonic_pin_3_trig = 12
ultrasonic_pin_3_echo = 13
ultrasonic_pin_4_trig = 15
ultrasonic_pin_4_echo = 16


infrared_pin_1 = 
infrared_pin_2 = 
infrared_pin_3 =
infrared_pin_4 = 

servo_pin = 

motor_pin_1 = 
motor_pin_2 = 

# initializing the GPIO pins as input/output
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(ultrasonic_pin_1_echo, GPIO.IN) # setting ultrasonic echo pins as input
GPIO.setup(ultrasonic_pin_2_echo, GPIO.IN)
GPIO.setup(ultrasonic_pin_3_echo, GPIO.IN)
GPIO.setup(ultrasonic_pin_4_echo, GPIO.IN)

GPIO.setup(ultrasonic_pin_1_trig, GPIO.OUT) # setting ultrasonic trigger pins as output
GPIO.setup(ultrasonic_pin_2_trig, GPIO.OUT)
GPIO.setup(ultrasonic_pin_3_trig, GPIO.OUT)
GPIO.setup(ultrasonic_pin_4_trig, GPIO.OUT)

GPIO.setup(ultrasonic_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(ultrasonic_pin_2, GPIO.IN)
GPIO.setup(ultrasonic_pin_3, GPIO.IN)
GPIO.setup(ultrasonic_pin_4, GPIO.IN)

GPIO.setup(servo_pin, GPIO.OUT) # setting servo pin as output

GPIO.setup(motor_pin_1, GPIO.OUT) # setting motor pins as output
GPIO.setup(motor_pin_2, GPIO.OUT)

# mobility system function
