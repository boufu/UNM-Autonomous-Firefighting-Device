# import library
import RPi.GPIO as GPIO
import time

# initialize pins
pump_pin = 36 # pin for the water pump
print("Pins initialized")

# setting up the pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump_pin, GPIO.OUT)
print("Pump pins setup complete!")

def pump_start():
  """Turn on the pump"""
  print("Pump start!")
  GPIO.output(pump_pin, GPIO.HIGH) # turn on pump

def pump_stop():
  """TUrn off the pump"""
  print("Pump stopped!")
  GPIO.output(pump_pin, GPIO.LOW)

try:
  while True:
    pump_start()
    time.sleep(6)
    pump_start()
    time.sleep(3)

except KeyboardInterrupt:
  GPIO.cleanup()
  print("Program stopped by user.")
