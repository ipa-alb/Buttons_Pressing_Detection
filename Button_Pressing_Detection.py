#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:53:33 2021

@author: ubuntu
"""

import RPi.GPIO as GPIO  

import time
import datetime
import threading
import Button_Pressing_Detection_parameter as RET_Param
import config

class Btn_Pressing_Detection(threading.Thread,RET_Param.RET_Parameter):
    def __init__(self, parameter,Btn):
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.Btn = Btn
        pass

    def my_callback_Btn(self,channel):                
        print self.Btn.Btn_name  # To see on the shell if we match with the Btn Pressing noise # To see on the shell if we match with the Btn Pressing noise
        self.parameter.time_Btn_Pressed= datetime.datetime.utcnow() # Log the time of the Btn Pressing in another module so it can be easily found
        self.Btn.Btn_send_information = True #enable the Thread_Send_Btn_State to send the socket message
        
        

    def run(self):
        time_start= time.time()
        time_end = time.time()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Btn.Btn_Port, GPIO.IN,pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.Btn.Btn_Port, GPIO.BOTH, callback=self.my_callback_Btn, bouncetime = self.Btn.bouncetime)  
        while config.stop_thread == False and (time_end - time_start < config.RET_time):
            time.sleep(1)
            time_end=time.time()
        if time_end - time_start < config.RET_time:
            config.stop_thread = True
        GPIO.cleanup()
        print("GPIO Port are cleant")
        print("RET has been running for : ",time_end - time_start)
#        try:
#            sleep(config.RET_time)         # DEFINE THE TIME OF SIMULATION
#            print "Time's up. Finished!"  
#        except KeyboardInterrupt:
#            GPIO.cleanup()
#            print("GPIO Port are cleant")
#        finally:                   # this block will run no matter how the try block exits  
#            GPIO.cleanup()         # clean up after yourself  
#            print("GPIO Port are cleant")
#        pass
 



