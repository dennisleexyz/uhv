#!/usr/bin/env python3

import RPi.GPIO as GPIO
from sshkeyboard import listen_keyboard
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor A
ena = 18  # Motor A speed control
motorA_pin1 = 17
motorA_pin2 = 22

# Motor B
enb = 13  # Motor B speed control
motorB_pin1 = 24
motorB_pin2 = 23

# Setup the motor pins as outputs
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.setup(motorA_pin1, GPIO.OUT)
GPIO.setup(motorA_pin2, GPIO.OUT)
GPIO.setup(motorB_pin1, GPIO.OUT)
GPIO.setup(motorB_pin2, GPIO.OUT)

# Initialize PWM
pwmA = GPIO.PWM(ena, 1000)  # Initialize PWM on ena 1000Hz frequency
pwmB = GPIO.PWM(enb, 1000)  # Initialize PWM on enb 1000Hz frequency

# Start PWM with a defined speed
speed = 100
pwmA.start(speed)  # Adjust this value between 0-100 to control speed
pwmB.start(speed)  # Adjust this value between 0-100 to control speed

def motors_forward():
    GPIO.output(motorA_pin1, GPIO.LOW)
    GPIO.output(motorA_pin2, GPIO.HIGH)
    GPIO.output(motorB_pin1, GPIO.LOW)
    GPIO.output(motorB_pin2, GPIO.HIGH)
    print("Moving forward")

def motors_backward():
    GPIO.output(motorA_pin1, GPIO.HIGH)
    GPIO.output(motorA_pin2, GPIO.LOW)
    GPIO.output(motorB_pin1, GPIO.HIGH)
    GPIO.output(motorB_pin2, GPIO.LOW)
    print("Moving backward")
    
def motors_left():
    GPIO.output(motorA_pin1, GPIO.HIGH)
    GPIO.output(motorA_pin2, GPIO.LOW)
    GPIO.output(motorB_pin1, GPIO.LOW)
    GPIO.output(motorB_pin2, GPIO.HIGH)
    print("Moving left");
    
def motors_right():
    GPIO.output(motorA_pin1, GPIO.LOW)
    GPIO.output(motorA_pin2, GPIO.HIGH)
    GPIO.output(motorB_pin1, GPIO.HIGH)
    GPIO.output(motorB_pin2, GPIO.LOW)
    print("Moving right");

def stop_motors():
    GPIO.output(motorA_pin1, GPIO.LOW)
    GPIO.output(motorA_pin2, GPIO.LOW)
    GPIO.output(motorB_pin1, GPIO.LOW)
    GPIO.output(motorB_pin2, GPIO.LOW)
    print("Motors stopped")

def on_press(key):
    global speed
    try:
        if key == 'w':  # Forward
            motors_forward()
        elif key == 's':  # Backward
            motors_backward()
        elif key =='a':
            motors_left();
        elif key == 'd':
            motors_right();
        elif key == 'j':  # Backward
            speed -= 10
            if speed <= 10:
                    speed = 0
            print(f'PWM = {speed}')
        elif key == 'k':  # Backward
            speed += 10
            if speed >= 100:
                    speed = 100
            print(f'PWM = {speed}')
        pwmA.start(speed)
        pwmB.start(speed)

    except AttributeError:
        pass

def on_release(key):
    if key == 'esc':
        # Stop listener and PWM
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()
        return False
    stop_motors()

# Collect events until released
with listen_keyboard(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
