#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:53:33 2021

@author: ubuntu
"""

#@file Button_Pressing_parameter.py
#
#@section libraries_Button_Pressing_Detection_RET Libraries/modules
# Custom class:
#   - Button_Definition in config_test
#   - Button_Pressing_Detection_parameter
# Standard library:
#   - RPi.GPIO : the high level Api that enables to communicate with the microcontrollers of the RPi
#   - time
#   - datetime
#   - threading

import RPi.GPIO as GPIO  

import time
import datetime
import threading
import Button_Pressing_Detection_parameter as RET_Param
import config_test


class Btn_Pressing_Detection(threading.Thread):
    """! The Btn_Pressing_Detection base class.
    Defines the thread that is detecting the button pressing
    """
    def __init__(self,parameter,Btn):
        """! The The Btn_Pressing_Detection class initializer
        @param parameter the parameter that the Btn_Pressing_Detection has to deal with
        @param Btn the button that teh Btn_Pressing_Detection is applied to
        @return a thread that detects the button pressing 
        """
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

    def get_times_Btn_change_state(self):
        """! The The Btn_Pressing_Detection get_time_Btn_change_state function
        @return the change of state of the button, for how long it was pressed and the datetime it is not pressed anymore 
        """
        if GPIO.input(self.Btn.Btn_Port)==0 and self.former_state == 1:
            self.current_state = 0
            if self.current_state != self.former_state :
                print(self.Btn.Btn_name,"is pushed ",self.counting)
                self.former_state = 0
                self.time_push_detected = time.time()
                self.parameter.time_Btn_Pressed= datetime.datetime.utcnow()
                self.Btn.Btn_send_information = True
        if GPIO.input(self.Btn.Btn_Port)==1 and self.former_state == 0:
            self.current_state = 1
            if self.current_state != self.former_state :
                print(self.Btn.Btn_name,"is UNpushed ",self.counting)
                self.former_state = 1
                self.counting +=1
                self.time_unpush_detected = time.time()
#                print("time between push and unpushed = ", self.time_between_push_unpushed)
#                self.time_between_push_unpushed = self.time_unpush_detected - self.time_push_detected
                time.sleep(0.05)

    def run(self):
        """! The The Btn_Pressing_Detection run
        @return a loop fort the thread to run in or stop the test when the time of the test is completed
        """
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
        return ("the RET is over")


