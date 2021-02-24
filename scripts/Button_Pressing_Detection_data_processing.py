#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:54:44 2021

@author: ubuntu
"""

#@file Button_Pressing_Detection_data_processing.py
#
#@ section Button_Pressing_Detection_data_processing_description Description
# This application is the data processing. In the Rpi, we do not want to have too much information. Therefore, the only information we are keeping is 
# the success of the event: We have detected a button pressure while the robot end effector is inside the button area.
# We have put their the real-time processing and the user must chose if he wants the RET application to be stopped from the Rpi or the computer.
#
#@section libraries_Button_Pressing_Detection_socket Libraries/modules
# Custom class:
#   - Button_Pressing_Detection_parameter
#   - config_test
# Standard library:
#   - datetime
#   - InfluxDBClient
#   - threading
#@section Button_Pressing_Detection_data_processing_todo
# Link the influxdb of the Rpi with the Influxdb of the computer
# Both are local databases not connected to the cloud, however there could be a solution to link them without creating a cloud account.

import datetime
import Button_Pressing_Detection_parameter as RET_Param
from influxdb import InfluxDBClient
import threading
import config_test

class Rpi_data_processing_RET(threading.Thread,RET_Param.RET_Parameter,InfluxDBClient):
    """! The Rpi_data_processing_RET base class.
    Defines the thread that is receiveing message from the computer
    """
    def __init__(self,parameter):
        """! The Rpi_data_processing_RET class initializer
        @param parameter the parameter that the Btn_Pressing_Detection has to deal with
        @return a thread that receives the message from the computer 
        """
        threading.Thread.__init__(self)
        self.client = InfluxDBClient(host="localhost",port="8086")
        self.L=[str(datetime.datetime.utcnow()), 'Btn1', 'touched', True]
        self.l=[str(datetime.datetime.utcnow()), 'Btn1', 'touched', False]
        self.t1 = datetime.datetime.strptime(self.L[0],'%Y-%m-%d %H:%M:%S.%f')
        self.t2 = datetime.datetime.strptime(self.L[0],'%Y-%m-%d %H:%M:%S.%f')
        self.time_zero = datetime.timedelta(0,0,0)
        self.data = []
        self.parameter = parameter ## does it work?
        pass
    
    def write_into_influxdb(self,parameter):
        """! The write_into_influxdb function
        @return the opening of the database we are gonna log the data in Influxdb
        """
        self.client.create_database(parameter.influxdb)
#        print(self.client.get_list_database())
        self.client.switch_database(parameter.influxdb)
        print("We have switched into the right database")
    
    def split_socketmsg_into_jsonbody(self,list_msg_to_write_into_influxdb):
        """! The write_into_influxdb function
        @param list_msg_to_write_into_influxdb the list we want to write in Influxdb
        @return the data we can write in Influxdb
        """
        if list_msg_to_write_into_influxdb[3] == False:
            requestType = "Error"
        else:
            requestType = "Success"
        self.data = [
                {
                    "measurement": self.parameter.influxdb_measurement, # choosing the name of the measurements before a test
                    "tags": {
                        "requestName": "Btn_State_Test",
                        "requestType": requestType
                    },
                    "time":list_msg_to_write_into_influxdb [0], # getting the time the button was pressed (detected by the Rpi)
                     "fields": {
                        "Btn_name": list_msg_to_write_into_influxdb [1],
                        "Btn_State": list_msg_to_write_into_influxdb [2],
                        "In_Time_Interval": list_msg_to_write_into_influxdb [3]
                                }
                }
            ]

    def write_data(self,data,client):
        """! The write_data function
        @param data the data we want to write in Influxdb
        @param client the Influxdb we are writing in
        @return the data we can write in Influxdb
        """        
        client.write_points(data)
    
    def compare_time(self,parameter):
        """! The compare_time function
        @param parameter the parameter we are working on
        @return a boolean corresponding to the detection if the button was pressed in the time interval the end effector was in the Button area
        """
        self.t1 = datetime.datetime.strptime(self.parameter.list_msg_entering_Btn_area[0],'%Y-%m-%d %H:%M:%S.%f') # have the string from the message back to the format we want to compare with
        self.t2 = datetime.datetime.strptime(self.parameter.list_msg_leaving_Btn_area[0],'%Y-%m-%d %H:%M:%S.%f')
        ## compare the time
        if (self.parameter.time_Btn_change_state - self.t1 > self.time_zero and self.parameter.time_Btn_change_state - self.t2 < self.time_zero):
        ## if True : write in db
            print ('Data Processed') # to see that we were able to compare time
            self.L[0]= self.parameter.time_Btn_change_state  # having the time the Btn_Pressed was detected by the Rpi
            self.L[1]= self.parameter.list_msg_leaving_Btn_area[1]
#            print(self.L)
            self.list_msg_to_write_into_influxdb = self.L
            self.split_socketmsg_into_jsonbody(self.L)
            self.write_data(self.data,self.client)
        else: ## else: stop the RET and print the error
            print('ERROR')
            self.l[0]=self.parameter.time_Btn_change_state
            self.l[1]= self.parameter.list_msg_leaving_Btn_area[1]
#            print(self.l)
            self.list_msg_to_write_into_influxdb = self.l
            self.split_socketmsg_into_jsonbody(self.l)
            self.write_data(self.data,self.client)
            if config_test.real_time_processing == True:
                print('ERROR detected with real_time_processing')
                self.parameter.stop_RET = True        
        pass
    
    def run(self):
        """! The Rpi_data_processing_RET run
        @return a loop for the thread to run in or stop the test when the time of the test is completed
        """
        self.write_into_influxdb(self.parameter)
        while config_test.stop_thread == False:
            if self.parameter.process_information == True:
                self.compare_time(self.parameter)
                self.parameter.process_information = False
            else:## else I wait
                pass


                
                



    
    