# this is the main code for the firefighting device #

# installing python libraries (need to install in the RBPi using its bash CLI) 
  # pip install RPi.GPIO

# importing libraries - might show yellow squiggly lines below...
# ...because I need to download the packages on the RBPi hardware not on my own laptop.
import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import Servo # import servo from gpiozero module 
import time

# initializing the GPIO pins as input/output
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

