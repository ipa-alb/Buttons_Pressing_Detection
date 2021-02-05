#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 08:47:41 2021

@author: ubuntu
"""

import RPi.GPIO as GPIO  
import time 
import threading
import csv

t0 = time.time()

class Btn_Pressing_Detection_Test(threading.Thread):
    def __init__(self,Btn_name,Btn_Port,acceleration_factor,velocity_factor,robot_settle_time):
        threading.Thread.__init__(self)
        # static
        self.name = Btn_name
        self.Port = Btn_Port      
        self.acceleration_factor = acceleration_factor
        self.velocity_factor = velocity_factor
        self.robot_settle_time = robot_settle_time
        # dynamic
        self.former_state = 1
        self.current_state = 1
        self.time_push_detected = time.time()
        self.time_unpush_detected = time.time()
        self.time_between_push_unpushed = time.time()
        self.counting = 0
        pass

    def get_times_Btn_change_state(self):
        if GPIO.input(self.Port)==0 and self.former_state == 1:
            self.current_state = 0
            if self.current_state != self.former_state :
                print(self.name,"is pushed ",self.counting)
                self.former_state = 0
                self.Btn_indicator = 0
                self.time_push_detected = time.time()
                time.sleep(0.05)
        if GPIO.input(self.Port)==1 and self.former_state == 0:
            self.current_state = 1
            if self.current_state != self.former_state :
                print(self.name,"is UNpushed ",self.counting)
                self.former_state = 1
                self.counting +=1
                self.time_unpush_detected = time.time()
                self.time_between_push_unpushed = self.time_unpush_detected - self.time_push_detected
                print("time between push and unpushed = ", self.time_between_push_unpushed)
                self.log_in_csv_file([self.time_between_push_unpushed])
                time.sleep(0.05)
        pass

    def log_in_csv_file(self,row):
        with open("/home/ubuntu/Buttons_Pressing_Detection/Btn_Pressing_Detection_Test/test_file/test_native_pilz_driver_3.csv","aw") as f:
            cr = csv.writer(f, delimiter=";",lineterminator="\n") 
            cr.writerow(row)
        pass

    def run(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Port, GPIO.IN,pull_up_down = GPIO.PUD_UP)
        while 1:
            try:
                self.get_times_Btn_change_state()
            except KeyboardInterrupt:
                GPIO.cleanup()
                print("GPIO Port are cleant")
                break

Btn_Port_1 = 19
Btn_Port_2 = 29
acceleration_factor = 1
velocity_factor = 1.57
robot_settle_time = 0.5

if __name__=="__main__":
    th_Btn_Pressing_Detection_Test_1 = Btn_Pressing_Detection_Test("Btn1",Btn_Port_1,acceleration_factor,velocity_factor,robot_settle_time)
    th_Btn_Pressing_Detection_Test_2 = Btn_Pressing_Detection_Test("Btn2",Btn_Port_2,acceleration_factor,velocity_factor,robot_settle_time)
    th_Btn_Pressing_Detection_Test_1.start()
    th_Btn_Pressing_Detection_Test_2.start()

    
