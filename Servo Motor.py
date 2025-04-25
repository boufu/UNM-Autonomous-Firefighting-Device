from gpiozero import AngularServo
from time import sleep

"""From tests: min angle = 60; max angle = 160"""

# Initialize the servo on GPIO pin 13
# min_pulse_width and max_pulse_width may need to be adjusted for your servo
servo = AngularServo(13, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

servo.angle = 0 # set servo.angle to default position

# Function to set the servo angle
def set_angle(angle):
    servo.angle = angle
    sleep(1)

# Main program loop
try:
    while True:
        angle = int(input("Enter angle (0 to 180): "))  # User input for angle
        set_angle(angle)  # Set servo to entered angle
except KeyboardInterrupt:
    print("Program stopped by user")


    
