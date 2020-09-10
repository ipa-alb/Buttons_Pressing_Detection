#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 08:47:41 2021

@author: ubuntu
"""

import RPi.GPIO as GPIO  
import time 
import threading

t0 = time.time()

class Btn_Pressing_Detection_Test(threading.Thread):
    def __init__(self,Btn_Port,acceleration_factor,velocity_factor,robot_settle_time):
        threading.Thread.__init__(self)
        # static
        self.Port = Btn_Port      
        self.acceleration_factor = acceleration_factor
        self.velocity_factor = velocity_factor
        self.robot_settle_time = robot_settle_time
        # dynamic
        self.current_state = 0
        self.time_push_detected = time.time()
        self.time_unpush_detected = time.time()
        self.counting = 0
        self.time_between_change_of_state = time.time()
        pass

    def my_callback_Btn1(self,channel):  
        if self.current_state != GPIO.input(self.Port):
            self.current_state = GPIO.input(self.Port)
            self.counting +=1
            if self.current_state  == 1:
                print "UNpushed", self.counting
                self.time_unpush_detected = time.time()
                self.time_between_change_of_state = self.time_unpush_detected - self.time_push_detected
                print("the time between pushed and unpushed is = ", self.time_between_change_of_state)
                #write into csv file
            if self.current_state  == 0:
                print "pushed" , self.counting
                self.time_push_detected = time.time()


        
    def log_in_csv_file(self):
        pass

    def run(self):
        time_start= time.time()
        time_end = time.time()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Port, GPIO.IN,pull_up_down = GPIO.PUD_UP)
        self.current_state = GPIO.input(self.Port)
        GPIO.add_event_detect(self.Port, GPIO.BOTH, callback=self.my_callback_Btn1, bouncetime = 10) 
        while 1:
            try:
                time.sleep(300)
            except KeyboardInterrupt:
                GPIO.cleanup()
                print("GPIO Port are cleant")
                break
 

Btn_Port_1 = 19
Btn_Port_2 = 29
acceleration_factor = 1
velocity_factor = 1.57
robot_settle_time = 0.01

if __name__=="__main__":
    th_Btn_Pressing_Detection_Test_1 = Btn_Pressing_Detection_Test(Btn_Port_1,acceleration_factor,velocity_factor,robot_settle_time)
    th_Btn_Pressing_Detection_Test_2 = Btn_Pressing_Detection_Test(Btn_Port_2,acceleration_factor,velocity_factor,robot_settle_time)
    th_Btn_Pressing_Detection_Test_1.start()
    th_Btn_Pressing_Detection_Test_2.start()
    






    

