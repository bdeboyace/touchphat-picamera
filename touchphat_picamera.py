#!/usr/bin/env python

#pydrive info from https://medium.com/@annissouames99/how-to-upload-files-automatically-to-drive-with-python-ee19bb13dda

import touchphat
from picamera import PiCamera
from os import system
import sys
import signal
from twython import Twython
from time import sleep, strftime
import random
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )





camera = PiCamera()
camera.resolution = (512, 384)
fname = (strftime("%y-%b-%d_%H:%M"))
photo_name = "/home/pi/" + fname + ".jpg"





    
@touchphat.on_release('A')
def handle_touch(event):
    print('press a event start')
    for led in range(1,7):
        touchphat.led_on(led)
        sleep(0.25)
        touchphat.led_off(led)
    camera.capture(photo_name)

@touchphat.on_touch('D')
def handle_touch(event):
    print('press D event start')
    for led in range(1,7):
        touchphat.led_on(led)
        sleep(0.25)
        camera.capture('image{0:04d}.jpg'.format(led))
        touchphat.led_off(led)
        sleep(0.25)
        
    system('convert -delay 20 -loop 0 image*.jpg animation.gif')
    touchphat.all_on()
    sleep(0.25)
    touchphat.all_off()
    sleep(0.25)
    touchphat.all_on()
    sleep(0.25)
    touchphat.all_off()
    print('finished converting to gif animation')
    

@touchphat.on_release('Enter')
def handle_touch(event):
    touchphat.led_on("Enter")
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
    message = "Selfie-gif at this #PatriotPi #Rjam on a RPi zero with TouchPhat and Camera module"
    image = open('animation.gif', 'rb')
    response = twitter.upload_media(media=image)
    media_id = [response['media_id']]
    twitter.update_status(status=message, media_ids=media_id)
    
    touchphat.led_off("Enter")
    touchphat.all_on()
    sleep(0.25)
    touchphat.all_off()
    sleep(0.25)
    touchphat.all_on()
    sleep(0.25)
    touchphat.all_off()
    print('I think it just tweeted. IDK go check it')




signal.pause()
