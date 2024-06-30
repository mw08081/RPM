
import RPi.GPIO as gp
import time

pins = [16,20,21]
gp.setmode(gp.BCM)

for pin in pins :
    gp.setup(pin, gp.OUT)

for pin in pins :
    gp.output(pin, True)
input()
for pin in pins :
    gp.output(pin, False)
