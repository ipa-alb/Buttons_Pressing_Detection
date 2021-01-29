#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:33:42 2021

@author: ubuntu
"""

#@file RET_main.py
#
#@brief Define the global variable that the Button Pressing Detection is using.
# You are defining the name of the databases where you want to write and the position of the button in the robot cell and their port on the Rpi


stop_thread = False
RET_time = 44000

## config of the parameter
acceleration_factor = 1
velocity_factor= 1.57
robot_settle_time = 0.01
dx = 0.06
dy = 0.05
dz = 0.02

## config of the socket
socket_host = '10.4.11.117'
socket_port = 5004

## config of the Influxdb
influxdb = "RET_Test"
influxdb_host = "localhost"
influxdb_port = "8086"


class Button_Definition():
    """! The Button_Definition_class
    Defines the class for each button that we are gonna work on
    """
    def __init__(self,port,name,x,y,z):
        """! The Button_Definition class initializer
        @param port The Gpio port that the button is connected to
        @param name The name we have given to the button
        @param x The x coordinate of the button
        @param y The y coordinate of the button
        @param z The z coordinate of the button
        @return an instance of the Button_Definition class  
        """
        self.Btn_Port = port
        self.Btn_name = name
        self.Btn_send_information = False
        self.x = x
        self.y = y
        self.z = z
        pass

x1 = -0.1
y1 = -0.45
z1 = 0.159
x2 = 0.05
y2 = -0.45
z2 =0.159
Btn1_name = "Btn1"
Btn2_name = "Btn2"


Btn1 = Button_Definition(29,Btn1_name,x1,y1,z1)
Btn2 = Button_Definition(19,Btn2_name ,x2,y2,z2)

## config RET with two buttons
list_two_buttons_RET = [Btn1,Btn2]

