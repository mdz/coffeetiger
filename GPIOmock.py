'''
Created on Oct 1, 2012

@author: lnobili
'''

BOARD = 0
OUT = 0
IN = 0
PUD_UP = 0
HIGH = 1
LOW = 0
BCM = 11

def setmode(something):
    pass

def setup(something1, something2, pull_up_down = 0):
    pass

last_value = {}
def input(pin):
    if pin in last_value:
      last_value[pin] += 1
    else:
      last_value[pin] = 0

    value = last_value[pin]

    print("GPIO input: {} = {}".format(pin, value))
    return value

def output(pin, value):
    if value == HIGH:
        print("GPIO output: {} = On".format(pin))
    else:
        print("GPIO output: {} = Off".format(pin))

def cleanup():
    pass
