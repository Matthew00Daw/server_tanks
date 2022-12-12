#!/usr/bin/env pybricks-micropython
from curses.ascii import US
from distutils.command.check import SilentReporter
import math
import pybricks 

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait, StopWatch

MAX_ANGLE = 30

TRANSLATION_SPEED = 100
ROTATION_SPEED = 50

Gsensor = GyroSensor(Port.S1, Direction.COUNTERCLOCKWISE)
Gsensor.reset_angle(0)
Csensor = ColorSensor(Port.S2)
motorL = Motor(Port.A)
motorR = Motor(Port.D, Direction.COUNTERCLOCKWISE)
motorC = Motor(Port.B)
Usensor = UltrasonicSensor(Port.C)
timer = StopWatch()

#timer = StopWatch()
last_error = 0
speed_add = 0

def regulate_rotate_speed(err):
    global last_error
    
    retval = 9.6*err + 2.4*(last_error-err)
    
    last_error = err
    return math.floor(retval)

def rotate_robot(angle):
    motorL.run(0)
    motorR.run(0)

    while Gsensor.angle != angle:
        new_speed = regulate_rotate_speed(angle-Gsensor.angle())
        motorL.run(new_speed)
        motorR.run(new_speed)
        brick.display.clear()
        brick.display.text(new_speed, (60, 50))
        brick.display.text(Gsensor.angle())
        #wait(10)

    motorR.stop()
    motorL.stop()

def measure_color():
    while not any(brick.buttons()):
        refl = Csensor.reflection()
        brick.display.clear()   
        brick.display.text(refl, (60, 50))


def translate(reset_offset=False):
    global speed_add
    if reset_offset:
        speed_add = 0
        motorL.run(TRANSLATION_SPEED)
        motorR.run(-TRANSLATION_SPEED)
    else:
        speed_add += 1
        motorL.run(TRANSLATION_SPEED + speed_add)
        motorR.run(-TRANSLATION_SPEED - speed_add)

def rotate(to_right = True):
    speed = (-1 if to_right else 1)*ROTATION_SPEED
    motorL.run(speed)
    motorR.run(speed)

def find_black(double_angle=False):
    color_found = False
            # right
    while abs(Gsensor.angle()) < (30 if not double_angle else 2*30):
        brick.display.clear()
        brick.display.text(Gsensor.angle(), (60, 50))
        if Csensor.reflection() < 50:
            color_found = True
            break
    return color_found

def drive_on_colour():
    is_moving = False
    right_rot = False
    timer.reset()
    while not any(brick.buttons()):
        refl = Csensor.reflection()
        if refl <= 50:
            if not is_moving:
                is_moving = True
                translate()
            else:
                if timer.time() > 100:
                    translate(False)
                    timer.reset()
        elif refl > 50:
            is_moving = False
            Gsensor.reset_angle(0)
            if right_rot:
                rotate(True)
                color_found = find_black()

                if color_found:
                    right_rot = True
                    continue
                Gsensor.reset_angle(0)

                rotate(False)
                find_black(True)
                right_rot = False
            else:
                rotate(False)
                color_found = find_black()

                if color_found:
                    right_rot = False
                    continue
                Gsensor.reset_angle(0)

                rotate(True)
                find_black(True)
                right_rot = True
            timer.reset()
    motorR.stop()
    motorL.stop()

       
def barrier_checking():
    motorR.run(0)
    motorL.run(0)
    motorC.run(0)
    distance = Usensor.distance(silent=True)
    noBarrier = True
    
    while not any(brick.buttons()):
        if distance < 100:
            brick.display.clear()
            brick.display.text("It's barrier ahead")

        

    motorR.stop()
    motorL.stop()

barrier_checking