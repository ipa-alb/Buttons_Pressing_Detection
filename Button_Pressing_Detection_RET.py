#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:51:34 2021

@author: ubuntu
"""
import Button_Definition
import Button_Pressing_Detection_parameter
import Button_Pressing_Detection_socket 
import Button_Pressing_Detection_data_processing
import Button_Pressing_Detection

def main():
    Btn1 = Button_Definition.Button_Definition(29,"Btn1",500,0,0,0)
    Btn2 = Button_Definition.Button_Definition(19,"Btn2",500,0,0,0)
    list_button=[Btn1,Btn2]
    # create an instance of Button_Pressing_Detection_Parameter
    parameter = Button_Pressing_Detection_parameter.RET_Parameter(list_button)
    parameter.define_measurement()
    if parameter.stop_RET == True:
        print "The program is ended"
        return 0
    ## launch the daemon that process the information
    th_data_processing = Button_Pressing_Detection_data_processing.Rpi_data_processing_RET(parameter)
    th_data_processing.setDaemon(True)
    th_data_processing.start()
    th_Button_Pressing_Detection_Btn1 = Button_Pressing_Detection.Btn_Pressing_Detection(parameter,Btn1)
    th_Button_Pressing_Detection_Btn1.start()
    th_Button_Pressing_Detection_Btn2 = Button_Pressing_Detection.Btn_Pressing_Detection(parameter,Btn2)
    th_Button_Pressing_Detection_Btn2.start()
    # create an instance of Button_Pressing_Detection_Parameter_socket that hereditate from the Button_Pressing_Detection_Parameter
    socket_server = Button_Pressing_Detection_socket.Rpi_SocketServer_RET(parameter)
    socket_server.open_socket_connection()
    

if __name__ == "__main__":
    main()