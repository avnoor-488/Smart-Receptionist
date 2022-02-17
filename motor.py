from PIL import Image
import base64
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
##from smbus import SMBus
import math
import cv2
import time
import shutil
import sys
from glob import glob
from subprocess import check_output, CalledProcessError
from servosix import ServoSix
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
m1 = 14
m2 = 15

GPIO.setup(m1,GPIO.OUT)
GPIO.setup(m2,GPIO.OUT)


##def motor():
GPIO.output(m1, True)
GPIO.output(m2, False)
time.sleep(1.5)
GPIO.output(m1, False)
GPIO.output(m2, False)
time.sleep(2)

GPIO.output(m1, False)
GPIO.output(m2, True)
time.sleep(1.5)
GPIO.output(m1, False)
GPIO.output(m2, False)
