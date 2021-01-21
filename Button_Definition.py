#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:27:17 2021

@author: ubuntu
"""

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