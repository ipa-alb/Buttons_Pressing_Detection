#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 11:16:07 2022

@author: ubuntu
"""


import socket
import time
import sys
import RPi.GPIO as GPIO
import datetime 
import config_test
#import Button_Pressing_Detection

host = "10.4.11.132"
port = 65432
             
former_state = 1
current_state = 1
time_push_detected = time.time()
time_unpush_detected = time.time()
time_between_push_unpushed = time.time()
counting = 0



def Send_message(n_of_messages):
    
     for i in range(1,n_of_messages): #Ersetze das hier mit einer Schleife die einfach ein Signal übergibt wenn die Buttons getestet werden.
           
         s.send("rpi;"+repr(time.time())+";1")
         time.sleep(0.5)
         s.send("rpi;"+repr(time.time())+";2")
         time.sleep(0.5)    
    
        
def Detect_BPressing():
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(29, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    former_state1 = 1
    former_state2 = 1
    current_state1 = 1
    current_state2 = 1
    time_push_detected1 = time.time()
    time_push_detected2 = time.time()
    counting1 = 0
    counting2 = 0
    
    while True:
        if GPIO.input(19)==0 and former_state1 == 1:
            current_state1 = 0
            if current_state1 != former_state1 :
                former_state1 = 0
                time_push_detected1 = time.time()
                print("Button 1 is pushed ",counting1," on time: ", time_push_detected1)
        if GPIO.input(19)==1 and former_state1 == 0:
            current_state1 = 1
            if current_state1 != former_state1 :
                #print("Button is Unpushed ",counting)
                former_state1 = 1
                counting1 +=1
                
#                print("time between push and unpushed = ", self.time_between_push_unpushed)
#                self.time_between_push_unpushed = self.time_unpush_detected - self.time_push_detected
                time.sleep(1)
                
        if GPIO.input(29)==0 and former_state2 == 1:
            current_state2 = 0
            if current_state2 != former_state2 :
                former_state2 = 0
                time_push_detected2 = time.time()
                print("Button 2 is pushed ",counting2," on time: ", time_push_detected2)
        if GPIO.input(29)==1 and former_state2 == 0:
            current_state2 = 1
            if current_state2 != former_state2 :
                #print("Button is Unpushed ",counting)
                former_state2 = 1
                counting2 +=1
                
#                print("time between push and unpushed = ", self.time_between_push_unpushed)
#                self.time_between_push_unpushed = self.time_unpush_detected - self.time_push_detected
                time.sleep(1)       
                
                
                
    

if __name__ == "__main__":
    try:
        print("1. starting the programm")
        print("2. creating socket object")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("3. creating connection")

        try: 
           # s.connect((host, port))
            print("4. Connection successfully created")
            Detect_BPressing() 
            
        except socket.error:
            print("4. Connection has failed")
            #s.close()
            sys.exit(0)
        
        
    except KeyboardInterrupt:
        
        print("Monitor Keyboard interrupted")
        s.close()
        sys.exit(0)
        
        