import sys
import RPi.GPIO as gpio
import time

pipe = None

#Motor 1 GPIO Pin
M1_A = 4
M1_B = 17

#Motor 2 GPIO Pin
M2_A = 27
M2_B = 22

gpio.cleanup()

gpio.setmode(gpio.BCM)

#Motor Pin Setup
gpio.setup(M1_A, gpio.OUT)
gpio.setup(M1_B, gpio.OUT)
gpio.setup(M2_A, gpio.OUT)
gpio.setup(M2_B, gpio.OUT)

def main():
    global pipe
    pipe = open('/dev/input/js0','r')

    print 'success'
    readJoystick()

def readJoystick():
    action = []

    while 1:
         for character in pipe.read(1):
                action += ['%02X' % ord(character)]

                if len(action) == 8:

                        num = int(action[5], 16) # Translate back to integer form
                        percent254 = str(((float(num)-128.0)/126.0)-100)[4:6] # Calculate the percentage of push
                        percent128 = str((float(num)/127.0))[2:4]

                        print '%s' % action

                        if percent254 == '.0':
                                percent254 = '100'
                        if percent128 == '0':
                                percent128 = '100'

                        if action[6] == '01': # Button
                                if action[4] == '01':
                                        print 'You pressed button: ' + action[7]
                                else:
                                        print 'You released button: ' + action[7]

                        elif action[7] == '00': # D-pad left/right
                                if action[4] == 'FF':
                                        print 'You pressed right on the D-pad'
                                        turnRight()
                                elif action[4] == '01':
                                        print 'You pressed left on the D-pad'
                                        turnLeft()
                                else:
                                        print 'You released the D-pad'
                                        stop()


                        elif action[7] == '01': # D-pad up/down
                                if action[4] == 'FF':
                                        print 'You pressed down on the D-pad'
                                        backword()
                                elif action[4] == '01':
                                        print  'You pressed up on the D-pad'
                                        forword()
                                else:
                                        print 'You released the D-pad'
                                        stop()


                        elif action[7] == '04': # Left Joystick left/right
                                if action[4] == 'FF':
                                        print 'You pressed right on the left joystick'
                                        turnRight()
                                elif action[4] == '01':
                                        print 'You pressed left on the left joystick'
                                        turnLeft()
                                else:
                                        print 'You released the left joystick'
                                        stop()

                        elif action[7] == '05': # Left Joystick up/down
                                if action[4] == 'FF':
                                        print 'You pressed down on the left joystick'
                                        backword()
                                elif action[4] == '01':
                                        print 'You pressed up on the left joystick'
                                        forword()
                                else:
                                        print 'You released the left joystick'
                                        stop()

                        elif action[7] == '02': # Right Joystick left/right
                                num = int(action[5], 16) # Translate back into integer form
                                if num >= 128:
                                        print 'You moved the right joystick left to %' + percent254
                                        turnLeft()
                                elif num <= 127 \
                                and num != 0:
                                        print 'You moved the right joystick right to %' + percent128
                                        turnRight()
                                else:
                                        print 'You stopped moving the right joystick'
                                        stop()

                        elif action[7] == '03': # Right Joystick up/ down
                                if num >= 128:
                                        print 'You moved the right joystick upward to %' + percent254
                                        forword()
                                elif num <= 127 \
                                and num != 0:
                                        print 'You moved the right joystick downward to %' + percent128
                                        backword()
                                else:
                                        print 'You stopped moving the right joystick'
                                        stop()
                        action = []

def forword():
    print 'GPIO Forward'
    gpio.output(M1_A, gpio.LOW)
    gpio.output(M1_B, gpio.HIGH)
    gpio.output(M2_A, gpio.LOW)
    gpio.output(M2_B, gpio.HIGH)

def backword():
    print 'GPIO Backward'
    gpio.output(M1_A, gpio.HIGH)
    gpio.output(M1_B, gpio.LOW)
    gpio.output(M2_A, gpio.HIGH)
    gpio.output(M2_B, gpio.LOW)

def turnLeft():
    print 'GPIO Turn Left'
    gpio.output(M1_A, gpio.LOW)
    gpio.output(M1_B, gpio.LOW)
    gpio.output(M2_A, gpio.LOW)
    gpio.output(M2_B, gpio.HIGH)

def turnRight():
    print 'GPIO Turn Right'
    gpio.output(M1_A, gpio.LOW)
    gpio.output(M1_B, gpio.HIGH)
    gpio.output(M2_A, gpio.LOW)
    gpio.output(M2_B, gpio.LOW)

def stop():
    print 'GPIO Stop'
    gpio.output(M1_A, gpio.LOW)
    gpio.output(M1_B, gpio.LOW)
    gpio.output(M2_A, gpio.LOW)
    gpio.output(M2_B, gpio.LOW)

if __name__ == "__main__":
    main()


