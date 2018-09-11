import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread

r = 255.0
g = 0.0
b = 0.0

state = True

pi = pigpio.pi()

def changeColor(color, step):
    color += step
    
    if color > 255:
        return 255
    if color < 0:
        return 0
        
    return color

def setLights(pin, brightness):
    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)

def getCh():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
    return ch

def checkKey():
    global bright
    global brightChanged
    global speedChanged
    global state
    global flash
    global abort
    global paused
    
    while True:
        c = getCh()
        
        if c == 'c' and not abort:
            abort = True
            break


start_new_thread(checkKey, ())

print ("+ / - = Increase / Decrease brightness")
print ("p / s / r = Pause Completely / Stop on Color / Resume")
print ("f = flash lights / d to go back to dimming fade")
print ("1 / 2 / 3 / 4 / 5 / 6 for different speeds")
print ("c = Abort Program")



setLights(RED_PIN, r)
setLights(GREEN_PIN, g)
setLights(BLUE_PIN, b)

while abort == False:
    if state:
        #Basically here just get the audio fft values then change colors 
        #based on those values instead of how this was done
        if r == 255 and b == 0 and g < 255:
                        
            g = updateColor(g, steps)
            setLights(GREEN_PIN, g)
        
        elif g == 255 and b == 0 and r > 0:
            r = updateColor(r, -steps)
            setLights(RED_PIN, r)
        
        elif r == 0 and g == 255 and b < 255:
            b = updateColor(b, steps)
            setLights(BLUE_PIN, b)
        
        elif r == 0 and b == 255 and g > 0:
            g = updateColor(g, -steps)
            setLights(GREEN_PIN, g)

        elif g == 0 and b == 255 and r < 255:
            r = updateColor(r, steps)
            setLights(RED_PIN, r)
        
        elif r == 255 and g == 0 and b > 0:
            b = updateColor(b, -steps)
            setLights(BLUE_PIN, b)
    
print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
