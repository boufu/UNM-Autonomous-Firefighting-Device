import RPi.GPIO as GPIO
from gpiozero import AngularServo
import time 

servo_pin = 32 # pin for the nozzle's servo motor 

pump_pin = 36 # pin for the water pump
print("... initial pins initialization complete!")
time.sleep(1)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump_pin, GPIO.OUT)
print ("... GPIO pins' INPUT and OUTPUT identification complete!")
time.sleep(1)


servo = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000) # uses BCM instead of board
print("Initialized servo motor at physical pin 32 (GPIO pin 12)")
time.sleep(1)


def pump_and_servo_start():
  """Starts pump and servo motor."""
  print("Pump and servo motor start!")
  GPIO.output(pump_pin, GPIO.HIGH) # turn on pump
  for i in range(3):
    position = 80
    counter = 0
    
    while counter < 3:
      position += 20
      servo.angle = position
      time.sleep(0.6)
      counter += 1
      print(position)

    counter = 0
    while counter < 6:
      position -= 20
      servo.angle = position
      time.sleep(0.6)
      counter += 1
    
    counter= 0
    while counter < 3:
      position += 20
      servo.angle = position
      time.sleep(0.6)
      counter += 1
  servo.angle = 90

def pump_and_servo_stop():
  """Turn off the pump and servo"""
  print("Pump stopped!")
  servo.angle = 90
  GPIO.output(pump_pin, GPIO.LOW)