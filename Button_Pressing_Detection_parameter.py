#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:55:11 2021

@author: ubuntu
"""
import datetime
import Button_Definition

class RET_Parameter(Button_Definition.Button_Definition):
    def __init__(self,list_button):
        #### Global Parameter of the RET
        self.time_begin_RET = datetime.datetime.utcnow()
        self.RET_driver = ""
        self.duration_RET = 12*60*60
        #### Parameter about the button Detection
        ##static parameter
        self.list_button = list_button
        self.list_name_Btn = ""
        self.list_bouncetime = []
        for i in range(len(self.list_button)):
            self.list_name_Btn += "_" + self    .list_button[i].Btn_name 
            self.list_bouncetime.append(self.list_button[i].bouncetime)
        ##changing parameter
        self.time_Btn_Pressed = datetime.datetime.utcnow()
        #### Parameter concerning the socket message
        ##static parameter
        self.socket_host = '10.4.11.117'
        self.socket_port = 5005
        self.x1 = 0.1
        self.y1 = -0.5
        self.z1 = 0.316
        self.x2 = 0.05
        self.y2 = -0.5
        self.z2 = 0.316
        self.dx = 0.06
        self.dy = 0.08
        self.dz = 0.05
        self.acceleration_factor = 1.7
        ##changing parameter
        self.list_msg_entering_Btn_area = []
        self.Btn_Unpressed_Time = datetime.datetime.utcnow()
        self.list_msg_leaving_Btn_area = []
        self.Btn_Pressed_in_Time_Interval = False
        #### Parameter that are to change during the RET concerning the data processing
        ##static parameter
        self.influxdb = "RET_Test"
        self.influxdb_measurement = "RET_Test_[" + str(self.x1) + ";" + str(self.y1) + ";" + str(self.z1) + "]_[" + str(self.x2) + ";" + str(self.y2) + ";" + str(self.z2) + "]_[" + str(self.dx) + ";" + str(self.dy) + ";" + str(self.dz) + "]_AccelerationFactor_[" + str(self.acceleration_factor) + "]" +self.list_name_Btn + "[" + str(self.list_bouncetime) + "]"
        self.influxdb_host = "localhost"
        self.influxdb_port = "8086"
        ##changing parameter
        self.write_into_measurement = False
        self.realtime_processing = True
        self.process_information = False
        self.stop_RET = False
    
    def define_measurement(self):
        ## print to the user what he is about to do
        print ("You are running the RET with the following parameter : ")
        print "Position Btn1= [", self.x1 ," ; ", self.y1, " ; ", self.z1, "] "
        print "Position Btn2= [", self.x2 ," ; ", self.y2, " ; ", self.z2, "] "
        print "Acceleration Factor = ", self.acceleration_factor 
        print "Writing in influxdb =: ", self.influxdb
        print "The real time processing is set to : ", self.realtime_processing, "\n"
        chose_driver=raw_input("ROS or native?")
        if chose_driver == "ROS":
            self.test_driver = "ROS"
        if chose_driver == "native":
            self.test_driver = "native"
        print("\nDo you want to continue?")
        ## add a raw input for the user to say if we are running the test with the ROS driver or with the native driver

        ## add a raw input for the user to say yes or no
        begin_test=raw_input("Y or N ?")
        if begin_test == "N":
            self.stop_RET = True
        else: 
            print "The RET begins at : ", self.time_begin_RET
            self.influxdb_measurement += self.RET_driver
            print "The data are logged in the measurement : ", self.influxdb_measurement   
        pass
    
    def print_information_running_RET(self):
        pass
    

if __name__ == "__main__":
    RET_Parameter = RET_Parameter()
    RET_Parameter = RET_Parameter.define_measurement()

