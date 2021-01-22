#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:33:42 2021

@author: ubuntu
"""

stop_thread = False
RET_time = 15

class Button_Definition():
    def __init__(self,port,name,bouncetime,x,y,z):
        self.Btn_Port = port
        self.Btn_name = name
        self.Btn_send_information = False
        self.bouncetime = bouncetime
        self.x = x
        self.y = y
        self.z = z
        pass

## config RET with two buttons
Btn1 = Button_Definition(29,"Btn1",500,0.1,-0.5,0.316)
Btn2 = Button_Definition(19,"Btn2",500,0.05,-0.5,0.316)

list_two_buttons_RET = [Btn1,Btn2]