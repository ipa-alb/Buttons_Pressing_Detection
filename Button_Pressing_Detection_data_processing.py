#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:54:44 2021

@author: ubuntu
"""
import datetime
import Button_Pressing_Detection_parameter as RET_Param
from influxdb import InfluxDBClient
import sys,threading
import config

class Rpi_data_processing_RET(threading.Thread,RET_Param.RET_Parameter,InfluxDBClient):
    def __init__(self,parameter):
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
        self.client.create_database(parameter.influxdb)
        print(self.client.get_list_database())
        self.client.switch_database(parameter.influxdb)
    
    def split_socketmsg_into_jsonbody(self,list_msg_to_write_into_influxdb):
        # Convert the list of information into json_body to enable writing in influxdb
        self.data = [
                {
                    "measurement": self.parameter.influxdb_measurement, # choosing the name of the measurements before a test
                    "tags": {
                        "requestName": "Btn_State_Test",
                        "requestType": "GET"
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
        client.write_points(data)
        pass
    
    def compare_time(self,parameter):
        self.t1 = datetime.datetime.strptime(self.parameter.list_msg_entering_Btn_area[0],'%Y-%m-%d %H:%M:%S.%f') # have the string from the message back to the format we want to compare with
        self.t2 = datetime.datetime.strptime(self.parameter.list_msg_leaving_Btn_area[0],'%Y-%m-%d %H:%M:%S.%f')
        ## compare the time
        if (self.parameter.time_Btn_Pressed - self.t1 > self.time_zero and self.parameter.time_Btn_Pressed - self.t2 < self.time_zero):
        ## if True : write in db
            print ('Btn was well pressed by the robot') # to see that we were able to compare time
            self.L[0]= self.parameter.time_Btn_Pressed  # having the time the Btn_Pressed was detected by the Rpi
            print(self.L)
            self.list_msg_to_write_into_influxdb = self.L
            self.split_socketmsg_into_jsonbody(self.L)
            self.write_data(self.data,self.client)
        else: ## else: stop the RET and print the error
            print('write into database error driver')
            self.l[0]=self.parameter.time_Btn_Pressed
            print(self.l)
            self.list_msg_to_write_into_influxdb = self.l
            self.split_socketmsg_into_jsonbody(self.l)
            self.write_data(self.data,self.client)
            self.parameter.stop_RET = True        
        pass
    
    def run(self):
        self.write_into_influxdb(self.parameter)
        while config.stop_thread == False:
            if self.parameter.process_information == True:
                print("Launch of the process")
                self.compare_time(self.parameter)
                self.parameter.process_information = False
            else:## else I wait
                pass


                
                



    
    