from gpiozero import AngularServo
from time import sleep

"""From tests: min angle = 60; max angle = 160"""

# Initialize the servo on GPIO pin 13
# min_pulse_width and max_pulse_width may need to be adjusted for your servo
servo = AngularServo(13, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

servo.angle = 90 # set servo.angle to default position
sleep(1)
steps = 30
increment = 30 / steps

# Function to set the servo angle
def set_angle():
        try:
                for i in range(3):
                        position = 80
                        counter = 0
                        
                        while counter < 3:
                                position += 20
                                servo.angle = position
                                sleep(0.6)
                                counter += 1
                                print(position)

                        counter = 0
                        while counter < 6:
                                position -= 20
                                servo.angle = position
                                sleep(0.6)
                                counter += 1
                        
                        counter= 0
                        while counter < 3:
                                position += 20
                                servo.angle = position
                                sleep(0.6)
                                counter += 1
                servo.angle = 90
        except KeyboardInterrupt:
                print("Program stopped by user")

# Main program loop
try:
    while True:
        set_angle()
        sleep(4)
except KeyboardInterrupt:
    print("Program stopped by user")


    
