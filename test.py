# test code for the IR sensors:
# the main problem with this code is that if more than 1 sensors picks up a HIGH signal, 
# the progam will fail unless a specific side is programmed to take precedence.


# import relevant libraries
import RPi.GPIO as GPIO
import time

# initialize ir sensors to the physical pins
IR_pin_1 = 7
IR_pin_2 = 8
IR_pin_3 = 9
IR_pin_4 = 10
print("IR pins initialized.")

# set these pins as input
GPIO.setmode(GPIO.board)
GPIO.setup(IR_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(IR_pin_2, GPIO.IN)
GPIO.setup(IR_pin_3, GPIO.IN)
GPIO.setup(IR_pin_4, GPIO.IN)
print("IR pins setup complete!")

# setting global variables for the IR_sensors readings
IR_sensor_1 = GPIO.LOW # setting all the IR sensors reading to be low initially
IR_sensor_2 = GPIO.LOW
IR_sensor_3 = GPIO.LOW
IR_sensor_4 = GPIO.LOW


# create fire detection flag
fire_detected = False # initial flag's state
print("Fire detection flag initialized and set to FALSE")

# define functions
def fire_detection_loop():
  """Reads IR sensor and changes fire_detected flag to true if there is a HIGH input"""
  IR_sensor_1 = GPIO.input(IR_pin_1) # read the sensor values
  IR_sensor_2 = GPIO.input(IR_pin_2)
  IR_sensor_3 = GPIO.input(IR_pin_3)
  IR_sensor_4 = GPIO.input(IR_pin_4)

  if any(IR_sensors_values > GPIO.HIGH for IR_sensors_values in [IR_sensor_1,IR_sensor_2, IR_sensor_3, IR_sensor_4]):
     fire_detected = True
     print("Fire detected!")
  else:
     fire_detected = False
     print("No fire detected...")
  
  return fire_detected

def fire_extinguishing_start():
  """Function that starts the fire extinguishing part"""
  IR_check = False
  Pos_check = False

  if  IR_sensor_1 == GPIO.HIGH:
    print("Fire in front of device!")
    while IR_check == False:
      servo_start()
      time.sleep(3)
      servo_stop()

      if GPIO.input(IR_pin_1) == GPIO.LOW:
         IR_check = True
      else:
         IR_check = False
    print("\tFire has been put out!")
  
  elif  IR_sensor_2 == GPIO.HIGH:
    print("Fire on the right of device!")
    while Pos_check == False:
      turn_right()

      if GPIO.input(IR_pin_1) == GPIO.HIGH:
          Pos_check = True
      else:
          Pos_check = False

    while IR_check == False:
      servo_start()
      time.sleep(3)
      servo_stop()
      
      if GPIO.input(IR_pin_1) == GPIO.LOW:
          IR_check = True
      else:
          IR_check = False
    print("\tFire has been put out!")
     
  elif  IR_sensor_4 == GPIO.HIGH:
    print("Fire on the left of device!")
    while Pos_check == False:
      turn_left()

      if GPIO.input(IR_pin_1) == GPIO.HIGH:
          Pos_check = True
      else:
          Pos_check = False

    while IR_check == False:
      servo_start()
      time.sleep(3)
      servo_stop()
      
      if GPIO.input(IR_pin_1) == GPIO.LOW:
          IR_check = True
      else:
          IR_check = False
      print("\tFire has been put out!")

  elif  IR_sensor_3 == GPIO.HIGH:
    print("Fire on the rear of device!")
    while Pos_check == False:
      turn_left()

      if GPIO.input(IR_pin_1) == GPIO.HIGH:
          Pos_check = True
      else:
          Pos_check = False

    while IR_check == False:
      servo_start()
      time.sleep(3)
      servo_stop()
      
      if GPIO.input(IR_pin_1) == GPIO.LOW:
          IR_check = True
      else:
          IR_check = False
      print("\tFire has been put out!")

# Main loop
try:
  while True:
    if fire_detected == False: # if fire is not detected
      fire_detection_loop() # and fire detection follows suit
    elif fire_detected == True: # however, the moment a fire is detected
      while fire_detected == True: # while the fire_detected flag is True
        fire_extinguishing_start() # the extinguishment will happen
        fire_detection_loop() # and the fire detection will follow suit
      servo_stop() # when the fire_detected flag turns False, while loop breaks and extinguishment stops 

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program stopped and GPIO cleaned up.")