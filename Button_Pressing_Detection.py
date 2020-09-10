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
import config_test

#class Btn_Pressing_Detection(threading.Thread,RET_Param.RET_Parameter):
#    def __init__(self, parameter,Btn):
#        threading.Thread.__init__(self)
#        self.parameter = parameter
#        self.Btn = Btn
#        pass
#
#    def my_callback_Btn(self,channel):                
#        print self.Btn.Btn_name  # To see on the shell if we match with the Btn Pressing noise # To see on the shell if we match with the Btn Pressing noise
#        self.parameter.time_Btn_Pressed= datetime.datetime.utcnow() # Log the time of the Btn Pressing in another module so it can be easily found
#        self.Btn.Btn_send_information = True #enable the Thread_Send_Btn_State to send the socket message
#        
#        
#
#    def run(self):
#        time_start= time.time()
#        time_end = time.time()
#        GPIO.setmode(GPIO.BOARD)
#        GPIO.setup(self.Btn.Btn_Port, GPIO.IN,pull_up_down = GPIO.PUD_UP)
#        GPIO.add_event_detect(self.Btn.Btn_Port, GPIO.BOTH, callback=self.my_callback_Btn, bouncetime = self.Btn.bouncetime)  
#        while config_test.stop_thread == False and (time_end - time_start < config_test.RET_time):
#            time.sleep(1)
#            time_end=time.time()
#        if time_end - time_start < config_test.RET_time:
#            config_test.stop_thread = True
#        GPIO.cleanup()
#        print("GPIO Port are cleant")
#        print("RET has been running for : ", time_end - time_start)


class Btn_Pressing_Detection(threading.Thread):
    def __init__(self,parameter,Btn):
        threading.Thread.__init__(self)
        # static
        self.parameter=parameter
        self.Btn = Btn     
        self.acceleration_factor = parameter.acceleration_factor
        self.velocity_factor = parameter.velocity_factor
        self.robot_settle_time = parameter.robot_settle_time
        # dynamic
        self.former_state = 1
        self.current_state = 1
        self.time_push_detected = time.time()
        self.time_unpush_detected = time.time()
        self.time_between_push_unpushed = time.time()
        self.counting = 0
        pass

    def get_times_Btn_change_state(self):
        if GPIO.input(self.Btn.Btn_Port)==0 and self.former_state == 1:
            self.current_state = 0
            if self.current_state != self.former_state :
                print(self.Btn.Btn_name,"is pushed ",self.counting)
                self.former_state = 0
                self.Btn_indicator = 0
                self.time_push_detected = time.time()
        if GPIO.input(self.Btn.Btn_Port)==1 and self.former_state == 0:
            self.current_state = 1
            if self.current_state != self.former_state :
                print(self.Btn.Btn_name,"is UNpushed ",self.counting)
                self.former_state = 1
                self.counting +=1
                self.time_unpush_detected = time.time()
                self.parameter.time_Btn_Pressed= datetime.datetime.utcnow()
                print("time between push and unpushed = ", self.time_between_push_unpushed)
                self.time_between_push_unpushed = self.time_unpush_detected - self.time_push_detected
                self.Btn.Btn_send_information = True
                time.sleep(0.05)

    def run(self):
        time_start= time.time()
        time_end = time.time()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Btn.Btn_Port, GPIO.IN,pull_up_down = GPIO.PUD_UP)
        while config_test.stop_thread == False and (time_end - time_start < config_test.RET_time):
            self.get_times_Btn_change_state()
            time_end = time.time()
            if time_end - time_start > config_test.RET_time:
                config_test.stop_thread = True
        GPIO.cleanup()
        print("GPIO Port are cleant")
        print("RET has been running for : ", time_end - time_start)


