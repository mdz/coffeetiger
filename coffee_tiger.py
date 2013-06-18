#!/usr/bin/env python
import time
import os

try:
  import RPi.GPIO as GPIO
except RuntimeError:
  print "Couldn't load RPi.GPIO, using mock instead"
  import GPIOmock as GPIO

import logging
import logging.handlers as handlers

"""
Thank you, Adafruit

http://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script

"""

GPIO.setmode(GPIO.BCM)
DEBUG = 1
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if ((adcnum > 7) or (adcnum < 0)):
    return -1

  GPIO.output(cspin, True)
 
  GPIO.output(clockpin, False) # start clock low
  GPIO.output(cspin, False) # bring CS low
 
  commandout = adcnum
  commandout |= 0x18 # start bit + single-ended bit
  commandout <<= 3 # we only need to send 5 bits here
  for i in range(5):
    if (commandout & 0x80):
      GPIO.output(mosipin, True)
    else:
      GPIO.output(mosipin, False)
    commandout <<= 1
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
 
  adcout = 0
  # read in one empty bit, one null bit and 10 ADC bits
  for i in range(12):
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
    adcout <<= 1
    if (GPIO.input(misopin)):
      adcout |= 0x1
 
  GPIO.output(cspin, True)
  adcout >>= 1 # first bit is 'null' so drop it
  return adcout
 
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
 
# 10k trim pot connected to adc #0
potentiometer_adc = 0;
 
last_read = 0 # this keeps track of the last potentiometer value
tolerance = 0 # to keep from being jittery we'll only change
# volume when the pot has moved more than 5 'counts'

class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        # If rotation/rollover is wanted, it doesn't make sense to use another
        # mode. If for example 'w' were specified, then if there were multiple
        # runs of the calling application, the logs from previous runs would be
        # lost if the 'w' is respected, because the log file would be truncated
        # on each run.
        if maxBytes > 0:
            mode = 'a'
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

# create logger
lgr = logging.getLogger('readings')

handler=SizedTimedRotatingFileHandler(
    'readings.txt', maxBytes=100, backupCount=5,
    when='s',interval=10,
    )
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the Handler to the logger
lgr.addHandler(handler)

lgr.setLevel(logging.INFO)
lgr.info("Logging initialized")
 
while True:
  # we'll assume that the pot didn't move
  trim_pot_changed = False
 
  # read the analog pin
  trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  # how much has it changed since the last read?
  pot_adjust = abs(trim_pot - last_read)
 
  if DEBUG:
    print "trim_pot:", trim_pot
    print "pot_adjust:", pot_adjust
    print "last_read", last_read
 
  if ( pot_adjust > tolerance ):
    trim_pot_changed = True
 
  if DEBUG:
    print "trim_pot_changed", trim_pot_changed
 
  if ( trim_pot_changed ):
    # log the current value
    lgr.info("The value is %d" % trim_pot)
 
  # save the potentiometer reading for the next loop
  last_read = trim_pot
  # hang out and do nothing for a half second
  time.sleep(0.5)
  
"""
Rotate the logs

http://stackoverflow.com/questions/8467978/python-want-logging-with-log-rotation-and-compression
"""
