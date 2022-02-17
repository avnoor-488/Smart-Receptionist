from PIL import Image
import base64
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import math
import cv2
import time
import shutil
import sys
from glob import glob
from subprocess import check_output, CalledProcessError
from servosix import ServoSix
import time
import requests
from urllib.request import urlopen

url = ''

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
m1 = 14
m2 = 15

button = 18

reset = 2
GPIO.setup(reset,GPIO.IN)

GPIO.setup(m1,GPIO.OUT)
GPIO.setup(m2,GPIO.OUT)

GPIO.setup(button, GPIO.IN)
lcd_rs        = 21 
lcd_en        = 20
lcd_d4        = 16
lcd_d5        = 12
lcd_d6        = 7
lcd_d7        = 8




lcd_columns = 16
lcd_rows    = 2


lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)

##back = True
camera=cv2.VideoCapture(0)

##def check_connectivity():
##    ret, frame = camera.read()
####    frame = increase_brightness(frame, 21)
##    print ('sending sample image')
##    t1 = datetime.now()
##    cv2.imwrite("pic2.jpeg", frame)
####    img = cv2.imread('/home/pi/automated irrigation/pic2.jpeg', 1)
####    cv2.imshow('img', img)
####    cv2.waitKey(1)
##    with open('pic2.jpeg', 'rb') as f:
##        en = base64.b64encode(f.read())
####    print (len(en))
##    data = {'img':en}

def check_connectivity():
    request_site = url + '1'
    ret, frame = camera.read()
##    frame = increase_brightness(frame, 21)
    print ('sending sample image')
    t1 = datetime.now()
    cv2.imwrite("pic2.jpeg", frame)
          ##    img = cv2.imread('/home/pi/automated irrigation/pic2.jpeg', 1)
          ##    cv2.imshow('img', img)
          ##    cv2.waitKey(1)
    with open('pic2.jpeg', 'rb') as f:
        en = base64.b64encode(f.read())
##    print (len(en))
    data = {'img':en}
    print(data)
    
    r = requests.post(request_site, data= data)
    data = r.text
    print(data)
    if data.find("Label1") > 0:
        index1 = data.find("Label1") + 8
        index2 = data.find("</span>")
        resp = data[index1:index2]
        print(resp)
        
##    print(r.text)
def response():
    req_site = url + '2' #+ '*' + '5' + '*' + '5'

    response = urlopen(req_site,timeout = 10)
    html = str(response.read())
    print (html)
    if html.find ("Label1") > 0:
        
        index1 = html.find("Label1") + 8
        index2 = html.find("</span>")
        resp = html[index1:index2]
        print(resp)
    ##print (html)
    return resp

        
def speak(text):
    os.system("pico2wave --lang=en-US -w sample2.wav \"" + text + "\" && aplay sample2.wav")
    os.remove("sample2.wav")
    
def door_bell():
    os.system("aplay /home/pi/smart_receptionist_with_smart_lock/Door_Bell.wav")

def motor():
    GPIO.output(m1, True)
    GPIO.output(m2, False)
    time.sleep(1)
    GPIO.output(m1, False)
    GPIO.output(m2, True)
    
##def interrupt_handler(channel):
##    global back
##    print("interrupt handler")
##    back = False
##    
##GPIO.add_event_detect(18, GPIO.FALLING,
##                  callback=interrupt_handler,
##                  bouncetime=1)


t3 = datetime.now()
while True:
      
    a = 0
    t2 = datetime.now()         
        
    main = True
    lcd.clear()
    lcd.message("   Smart\n Receptionist\n")
##    speak("Smart Receptionist with")
    time.sleep(2)
    lcd.clear()
    lcd.message(" Smart-lock\n   System ")
##    speak("Smart Receptionist, with, smart lock, System")
    time.sleep(2)
    
    t1 = datetime.now()
    
    while main and GPIO.input(reset) == True:

        if GPIO.input(button) == False:
            door_bell()
            check_connectivity()
            while True:
                a = response()
                time.sleep(2)
                t2 = datetime.now()
                delta = t2 - t1
                time_elapse = delta.total_seconds() 
                if  time_elapse < 5:
                    t1 = datetime.now()
                    print("Response not Given from the server")
                    break
                if a == '2'or a == '3':
                    print("Response available")
                    break
                
            if a == '2':
                print("  Door Unlocked ")
                lcd.clear()
                lcd.message(" Door Unlocked")
                time.sleep(2)
            elif a == '3':
                print("  Door Locked")
                lcd.clear()
                lcd.message(" Door Locked")
                time.sleep(2)
            else:
                print("No Action\nTaken")  
                
                
                    
                
        lcd.clear()
        lcd.message("Welcome ..")
        time.sleep(0.5)
