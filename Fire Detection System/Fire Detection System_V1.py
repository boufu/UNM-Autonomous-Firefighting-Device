import RPi.GPIO as GPIO # import GPi.GPIO package and alias it as GPIO
from gpiozero import AngularServo
import time

servo_pin = 32 # pin for the nozzle's servo motor 

pump_pin = 36 # pin for the water pump

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

GPIO.setup(pump_pin, GPIO.OUT)

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

servo = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000) # uses BCM instead of board
print("Initialized servo motor at physical pin 32 (GPIO pin 12)")
time.sleep(1)

servo.angle = 90
time.sleep(1)



fire_detected = False # initial flag's state

GPIO.output(pump_pin, GPIO.LOW) # set pump low initially



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

def stop_motors():
  """Function to stop motors"""
  motor_left_PWM.ChangeDutyCycle(0)
  motor_right_PWM.ChangeDutyCycle(0)
  print("Both motors have been disabled!")

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


# main loop

counter = 1

try:
  while True:
    print(f"\n-------------- Iteration: {counter} --------------")
    if fire_detected == False: # if fire is not detected
      fire_detection_loop() # and fire detection follows suit
      time.sleep(0.1)
    elif fire_detected == True: # however, the moment a fire is detected
      while fire_detected == True: # while the fire_detected flag is True
        fire_extinguishing_start() # the extinguishment will happen
        fire_detection_loop() # and the fire detection will follow suit 
        time.sleep(0.1)
    counter += 1
  

except KeyboardInterrupt:
  GPIO.cleanup()
  print("Program stopped by user.")
  

