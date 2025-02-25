# this is the main code for the firefighting device #

# installing python libraries (need to install in the RBPi using its bash CLI) 
  # pip install RPi.GPIO

# importing libraries - might show yellow squiggly lines below...
# ...because I need to download the packages on the RBPi hardware not on my own laptop.
import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import Servo # import servo from gpiozero module 
import time

# initializing pins (signal pins)
ultrasonic_pin_1 = 7  
ultrasonic_pin_2 = 8
ultrasonic_pin_3 = 10
ultrasonic_pin_4 = 11

infrared_pin_1 = 12
infrared_pin_2 = 13
infrared_pin_3 = 15
infrared_pin_4 = 16 

servo_pin = 18

motor_pin_1 = 19
motor_pin_2 = 21

# initializing the GPIO pins as input/output
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(ultrasonic_pin_1, GPIO.IN) # setting ultrasonic pins as input
GPIO.setup(ultrasonic_pin_2, GPIO.IN)
GPIO.setup(ultrasonic_pin_3, GPIO.IN)
GPIO.setup(ultrasonic_pin_4, GPIO.IN)

GPIO.setup(ultrasonic_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(ultrasonic_pin_2, GPIO.IN)
GPIO.setup(ultrasonic_pin_3, GPIO.IN)
GPIO.setup(ultrasonic_pin_4, GPIO.IN)

GPIO.setup(servo_pin, GPIO.OUT) # setting servo pin as output

GPIO.setup(motor_pin_1, GPIO.OUT) # setting motor pins as output
GPIO.setup(motor_pin_2, GPIO.OUT)

# mobility system function
