# test code for the IR sensors:
# the main problem with this code is that if more than 1 sensors picks up a HIGH signal, 
# the progam will fail unless a specific side is programmed to take precedence.


# import relevant libraries
import RPi.GPIO as GPIO
import time

# initialize ir sensors to the physical pins
IR_pin_1 = 21 # pins for the infrared sensors
IR_pin_2 = 24
IR_pin_3 = 26
IR_pin_4 = 23
print("IR pins initialized.")

# set these pins as input
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR_pin_1, GPIO.IN) # setting infrared pins as input
GPIO.setup(IR_pin_2, GPIO.IN)
GPIO.setup(IR_pin_3, GPIO.IN)
GPIO.setup(IR_pin_4, GPIO.IN)
print("IR pins setup complete!")

def test_IR():
  IR_sensor_1 = GPIO.input(IR_pin_1)
  IR_sensor_2 = GPIO.input(IR_pin_2)
  IR_sensor_3 = GPIO.input(IR_pin_3)
  IR_sensor_4 = GPIO.input(IR_pin_4)
  print(f"IR1 input is {IR_sensor_1}")
  print(f"IR2 input is {IR_sensor_2}")
  print(f"IR3 input is {IR_sensor_3}")
  print(f"IR4 input is {IR_sensor_4}")
  time.sleep(1)

try:
  while True:
    test_IR()
    time.sleep(1)
except KeyboardInterrupt:
  GPIO.cleanup
  print("Program stopped by user")
