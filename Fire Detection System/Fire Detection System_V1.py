import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
import time

IR_pin_1 = 21 # pins for the infrared sensors
IR_pin_2 = 24
IR_pin_3 = 26
IR_pin_4 = 23

motor_pin_left_PWM = 33 # pins for the motor
motor_pin_left_DIR = 29
motor_pin_right_PWM = 35
motor_pin_right_DIR = 31
print("... initial pins initialization complete!")
time.sleep(1)

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers 

GPIO.setup(IR_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(IR_pin_2, GPIO.IN)
GPIO.setup(IR_pin_3, GPIO.IN)
GPIO.setup(IR_pin_4, GPIO.IN)

GPIO.setup(motor_pin_left_PWM, GPIO.OUT) # setting motor pins PWM and DIR as output
GPIO.setup(motor_pin_left_DIR, GPIO.OUT)
GPIO.setup(motor_pin_right_PWM, GPIO.OUT)
GPIO.setup(motor_pin_right_DIR, GPIO.OUT)
print ("... GPIO pins' INPUT and OUTPUT identification complete!")
time.sleep(1)

motor_left_PWM = GPIO.PWM(motor_pin_left_PWM, 200) # 200 Hz PWM
motor_right_PWM = GPIO.PWM(motor_pin_right_PWM, 200) # 200 Hz PWM
motor_left_PWM.start(0) # start at neutral position
motor_right_PWM.start(0) # start at neutral position
print("The Motors' PWM has been enabled!")
time.sleep(1)

fire_detected = False # initial flag's state

# define functions
def fire_detection_loop():
  """Read IR sensors and compare against threshold value to detect fire and set off a flag"""
  IR1_reading = GPIO.input(IR_pin_1)
  IR2_reading = GPIO.input(IR_pin_2)
  IR3_reading = GPIO.input(IR_pin_3)
  IR4_reading = GPIO.input(IR_pin_4)

  if any( > threshold for ir_sensors in [, , , ]): # for all sensos above the threshold, fire_detected flag changes to True, otherwise change to False
    fire_detected = True
  else:
    fire_detected = False
