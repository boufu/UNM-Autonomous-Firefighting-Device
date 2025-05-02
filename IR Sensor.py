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

def test_IR():
  IR_sensor_1 = GPIO.input(IR_pin_1)
  IR_sensor_2 = GPIO.input(IR_pin_2)
  IR_sensor_3 = GPIO.input(IR_pin_3)
  IR_sensor_3 = GPIO.input(IR_pin_4)

  if IR_sensor_1 == GPIO.HIGH:
    print ("IR reading is HIGH!")
  else:
    print("No IR reading received")

try:
  while True:
    test_IR()
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup
  print("Program stopped by user")