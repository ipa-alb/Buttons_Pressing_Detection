#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:33:42 2021

@author: ubuntu
"""

stop_thread = False
RET_time = 6000

## config of the parameter
acceleration_factor = 1
velocity_factor= 1.57
robot_settle_time = 0.01
dx = 0.06
dy = 0.05
dz = 0.02

## config of the socket
socket_host = '10.4.11.117'
socket_port = 5002

## config of the Influxdb
influxdb = "RET_Test"
influxdb_host = "localhost"
influxdb_port = "8086"


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

Btn1 = Button_Definition(29,"Btn1",200,-0.1,-0.47,0.155)
Btn2 = Button_Definition(19,"Btn2",200,0.05,-0.47,0.155)

## config RET with two buttons
list_two_buttons_RET = [Btn1,Btn2]

