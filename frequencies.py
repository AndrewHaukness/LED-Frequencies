import matplotlib
matplotlib.use('Agg')

import sys
import SWHear

import scipy

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread

import scipy.io.wavfile as wavfile
import numpy as np
import pylab as pl


RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

#white default
bright = 255
r = 255.0
g = 255.0
b = 255.0

state = True
abort = False

print "started"

#ear = SWHear.SWHear(rate=44100,updatesPerSecond=20)
#ear.stream_start()
rate, data = wavfile.read('test.wav')
#t = np.arange(len(data[:,0]))*1.0/rate
#pl.plot(t,data[:0])
#pl.show()

p = 20*np.log10(np.abs(np.fft.rfft(data[:2048, 0])))
f = np.linspace(0, rate/2.0, len(p))
print(f)
pl.plot(f,p)
pl.xlabel("Frequency(Hz)")
pl.ylabel("Power(dB)")
pl.show()


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

print ("c = Abort Program")



setLights(RED_PIN, r)
setLights(GREEN_PIN, g)
setLights(BLUE_PIN, b)



while abort == False:
    if state:
        #Basically here just get the audio fft values then change colors 
        #based on those values instead of how this was done
        if r == 255 and b == 0 and g < 255:
                        
            g = changeColor(g, steps)
            setLights(GREEN_PIN, g)
        
        elif g == 255 and b == 0 and r > 0:
            r = changeColor(r, -steps)
            setLights(RED_PIN, r)
        
        elif r == 0 and g == 255 and b < 255:
            b = changeColor(b, steps)
            setLights(BLUE_PIN, b)
        
        elif r == 0 and b == 255 and g > 0:
            g = changeColor(g, -steps)
            setLights(GREEN_PIN, g)

        elif g == 0 and b == 255 and r < 255:
            r = changeColor(r, steps)
            setLights(RED_PIN, r)
        
        elif r == 255 and g == 0 and b > 0:
            b = changeColor(b, -steps)
            setLights(BLUE_PIN, b)
    
print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
