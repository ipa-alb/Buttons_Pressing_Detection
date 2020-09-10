#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:55:11 2021

@author: ubuntu
"""
import datetime
import config_test

class RET_Parameter(config_test.Button_Definition):
    def __init__(self,list_buttons):
        #### Global Parameter of the RET
        self.time_begin_RET = datetime.datetime.utcnow()
        self.RET_driver = ""
        self.start_RET = True
        self.stop_thread = False
        self.acceleration_factor = config_test.acceleration_factor
        self.velocity_factor = config_test.velocity_factor
        self.robot_settle_time = config_test.robot_settle_time
        #### Parameter about the button Detection
        ##static parameter
        self.list_buttons = list_buttons
        self.list_name_Btn = ""
        self.list_bouncetime = []
        self.list_buttons_positions = []
        for i in range(len(self.list_buttons)):
            list_button_positions=[]
            self.list_name_Btn += "_" + self.list_buttons[i].Btn_name 
            self.list_bouncetime.append(self.list_buttons[i].bouncetime)
            list_button_positions.append(list_buttons[i].x)
            list_button_positions.append(list_buttons[i].y)
            list_button_positions.append(list_buttons[i].z)
            self.list_buttons_positions.append(list_button_positions)
        ##changing parameter
        self.time_Btn_Pressed = datetime.datetime.utcnow()
        #### Parameter concerning the socket message
        ##static parameter
        self.socket_host = config_test.socket_host
        self.socket_port = config_test.socket_port
        self.dx = config_test.dx
        self.dy = config_test.dy
        self.dz = config_test.dz
        ##changing parameter
        self.list_msg_entering_Btn_area = []
        self.Btn_Unpressed_Time = datetime.datetime.utcnow()
        self.list_msg_leaving_Btn_area = []
        self.Btn_Pressed_in_Time_Interval = False
        #### Parameter that are to change during the RET concerning the data processing
        ##static parameter
        self.influxdb = config_test.influxdb
        self.influxdb_measurement = ("RET_Test_" + self.list_name_Btn + str(self.list_buttons_positions) + "_[" + str(self.dx) + ";" + 
        str(self.dy) + ";" + str(self.dz) +"_bouncetime_"+ "[" + str(self.list_bouncetime) + "]_AccelerationFactor_[" + str(self.acceleration_factor) +
        "]_VelocityFactor_[" + str(self.velocity_factor) + "]" + "_robot_settle_time_[" + str(self.robot_settle_time) + "]_")
        ## we can also add a date to the measurement for more precision
        self.influxdb_host = config_test.influxdb_host
        self.influxdb_port = config_test.influxdb_port
        ##changing parameter
        self.write_into_measurement = False
        self.realtime_processing = True
        self.process_information = False
        
    
    def define_measurement(self):
        ## print to the user what he is about to do
        print ("You are running the RET with the following parameter : ")
        for button in self.list_buttons:
            print button.Btn_name, "[", button.x," ; ", button.y, " ; ", button.z, "] "
        print "Acceleration Factor = ", self.acceleration_factor 
        print "Writing in influxdb =: ", self.influxdb
        print "The real time processing is set to : ", self.realtime_processing, "\n"
        chose_driver=raw_input("ROS or native?")
        if chose_driver == "ROS":
            self.RET_driver = "ROS"
        if chose_driver == "native":
            self.RET_driver = "native"
        print("\nDo you want to continue?")
        ## add a raw input for the user to say if we are running the test with the ROS driver or with the native driver

        ## add a raw input for the user to say yes or no
        begin_test=raw_input("Y or N ?")
        if begin_test == "N":
            self.start_RET = False
        else: 
            print "\nThe RET begins at : ", self.time_begin_RET
            self.influxdb_measurement += self.RET_driver
            print "The data are logged in the measurement : ", self.influxdb_measurement   
        pass
    
    def print_information_running_RET(self):
        pass
    

if __name__ == "__main__":
    RET_Parameter = RET_Parameter()
    RET_Parameter = RET_Parameter.define_measurement()

