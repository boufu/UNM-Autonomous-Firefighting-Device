# test code for the IR sensors:
# the main problem with this code is that if more than 1 sensors picks up a HIGH signal, 
# the progam will fail unless a specific side is programmed to take precedence.


# import relevant libraries
import RPi.GPIO as GPIO
import time

# initialize ir sensors to the physical pins
IR_pin_1 = 8
IR_pin_2 = 7
IR_pin_3 = 9
IR_pin_4 = 10
print("IR pins initialized.")

# set these pins as input
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR_pin_1, GPIO.IN) # setting infrared pins as input
print("IR pins setup complete!")


# create fire detection flag
fire_detected = False # initial flag's state
print("Fire detection flag initialized and set to FALSE")

def test_IR():
	IR_sensor_1 = GPIO.input(IR_pin_1)
	print(f"IR input is {IR_sensor_1}")

try:
  while True:
    test_IR()
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup
  print("Program stopped by user")
