import RPi.GPIO as GPIO
import time

pump_pin = 17  # GPIO pin connected to the servo signal wire

GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)

# Set PWM to 50Hz (servo motors usually work at 50Hz)
pwm = GPIO.PWM(pump_pin, 50)
pwm.start(0)  # Start with pulse off

def set_servo_angle(angle):
    """Converts an angle to a duty cycle and moves the servo"""
    duty_cycle = 2 + (angle / 18)  # convert angle to duty cycle (approximate)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.4)  # give the servo time to move

def extinguishing_activate(sweep_angle = 60, cycles = 3): # sweep_angle = angles to sweep for per cycle; cycles = number of cycles to sweep
  """Turns on pump and sweeps servo motor"""
  try:
    for i in range(cycles):
      set_servo_angle(120)  # move servo up
      set_servo_angle(0)  # move servo down

  except KeyboardInterrupt: # stop function if there's any keyboard input
    pass  # allow stopping with ctrl+c

def extinguishing_stop():
  """Turns off pump and returns servo motor to neutral position"""
  print("\nTurning off water pump...")
  pwm.ChangeDutyCycle(0)  # stop sending PWM signals

try:
    
    while True:
        extinguishing_activate()
        extinguishing_stop()
        time.sleep(2)
        
except KeyboardInterrupt:
    print("Stopped by User")
    pwm.stop()
    GPIO.cleanup()


