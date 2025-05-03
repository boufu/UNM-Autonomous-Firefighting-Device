import RPi.GPIO as GPIO
import time

motor_pin_left_PWM = 33 # pins for the motor
motor_pin_left_DIR = 29
motor_pin_right_PWM = 35
motor_pin_right_DIR = 31
print("Motor pins initialized!")
time.sleep(2)

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 
GPIO.setup(motor_pin_left_PWM, GPIO.OUT) # setting motor pins PWM and DIR as output
GPIO.setup(motor_pin_left_DIR, GPIO.OUT)
GPIO.setup(motor_pin_right_PWM, GPIO.OUT)
GPIO.setup(motor_pin_right_DIR, GPIO.OUT)
print("GPIO setup complete!")
time.sleep(2)

# initialize PWM for motor PWM pins
motor_left_PWM = GPIO.PWM(motor_pin_left_PWM, 200) # 200 Hz PWM
motor_right_PWM = GPIO.PWM(motor_pin_right_PWM, 200) # 200 Hz PWM
motor_left_PWM.start(0) # start at neutral position
motor_right_PWM.start(0) # start at neutral position
print("The Motors' PWM has been enabled!")
time.sleep(2)

def stop_motors():
  """Function to stop left motor"""
  motor_left_PWM.ChangeDutyCycle(0)
  motor_right_PWM.ChangeDutyCycle(0)
  print("Both motors have been disabled!")

def move_forward(speed=10, duration=1):
  """Function to move motors forward"""
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  print("Moving motors forward")
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  time.sleep(duration)
  stop_motors()

def move_backward(speed=10, duration=1):
  """Function to move motors backward"""
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)          
  print("Moving left motors backward")
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  time.sleep(duration)
  stop_motors()
  
def turn_left(speed=9, duration=7.7):
  """Function to turn left"""
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed) 
  print("Turning left")
  GPIO.output(motor_pin_left_DIR, GPIO.HIGH)
  GPIO.output(motor_pin_right_DIR, GPIO.LOW)
  time.sleep(duration)
  stop_motors()
  
def turn_right(speed=9, duration=7.7):
  """Function to turn right"""
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed) 
  print("Turning right")
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  time.sleep(duration)
  stop_motors()

try:
  move_forward()
  time.sleep(2)
  turn_left()
  time.sleep(2)
  move_forward()
  time.sleep(2)
except KeyboardInterrupt:
  GPIO.cleanup()
  print("Program stopped by user")
'''
# define functions
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
  stop_motors

def turn_right(speed=70, duration=0.1):
  """Function to move right motor in the reverse dir. and the left motor in the forward dir."""
  print("Turning right.")
  GPIO.output(motor_pin_left_DIR, GPIO.LOW)
  GPIO.output(motor_pin_right_DIR, GPIO.HIGH)
  motor_left_PWM.ChangeDutyCycle(speed)
  motor_right_PWM.ChangeDutyCycle(speed)
  time.sleep(duration)
  stop_motors()

# main loop:
'''
