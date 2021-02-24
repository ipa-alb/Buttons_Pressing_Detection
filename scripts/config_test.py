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
# We made a button class. Each button is an instance of the Button_Definition class.
# @section notes_configuration Notes
# We define the parameter of the button in this configuration file such as:
#   - the socket server port and host
#   - the Button area that is to be working: 
#   - the parameter that are thought to be useful to work on
#   - the real_time_processing 
#   - the time the Button_Pressing_Detection application is running
#
# @section todo_config
# Find a way to define the parameter on only one device. For now, the button instance are created on the computer and on the Rpi, but it would be better to
# open the socket communication. Once this socket communication is open, we create the buttons classes on only one device, and export it to the other device via 
# the socket.
real_time_processing = False
stop_thread = False
RET_time = 65000

## config of the parameter
acceleration_factor = 3.49
velocity_factor= 1.57
robot_settle_time = 0.2
dx = 0.06
dy = 0.06
dz = 0.01

## config of the socket
socket_host = '10.4.11.117'
socket_port = 5001

## config of the Influxdb
influxdb = "RET_Test"
influxdb_host = "localhost"
influxdb_port = "8086"


class Button_Definition():
    """! The Button_Definition_class
    Defines the class for each button that we are gonna work on. This class provide the ability to work with a plan of button
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
z1 = 0.145
x2 = 0.05
y2 = -0.45
z2 =0.145
Btn1_name = "Btn1"
Btn2_name = "Btn2"


Btn1 = Button_Definition(29,Btn1_name,x1,y1,z1)
Btn2 = Button_Definition(19,Btn2_name ,x2,y2,z2)

## config RET with two buttons
list_two_buttons_RET = [Btn1,Btn2]

