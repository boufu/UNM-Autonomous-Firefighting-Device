import RPi.GPIO as GPIO
import time

servo_pin = 17  # GPIO pin connected to the servo signal wire

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM to 50Hz (servo motors usually work at 50Hz)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)  # Start with pulse off

def set_angle(angle):
    duty = 2 + (angle / 18)  # Convert angle (0–180) to duty cycle
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)  # Avoid buzzing or jittering

try:
    while True:
        set_angle(0)
        time.sleep(1)
        set_angle(90)
        time.sleep(1)
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by User")
    pwm.stop()
    GPIO.cleanup()

