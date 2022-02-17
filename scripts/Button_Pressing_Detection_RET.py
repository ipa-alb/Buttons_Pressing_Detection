#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:51:34 2021

@author: ubuntu
"""
"""!@brief Define the Button Pressing Detection for the RET."""
##
# @mainpage Button Pressing Detection RET 
# @section description_main Description
# The application is meant to run for the RET and will communicate with the computer driving the robot that you are testing.
# The Button Pressing Detection application is processing the data regarding the button pressing and the data received by the computer.
#@section notes_main Notes
#
# @Copyright (c) 2021 Alban Boytard. All rights reserved
##
#@file RET_main.py
#
#@section libraries_Button_Pressing_Detection_RET Libraries/modules
# Custom class:
#   - Button_Pressing_Detection_parameter
#   - Button_Pressing_Detection_socket 
#   - Button_Pressing_Detection_data_processing
#   - Button_Pressing_Detection
#   - config_test


import Button_Pressing_Detection_parameter
import Button_Pressing_Detection_socket 
import Button_Pressing_Detection_data_processing
import Button_Pressing_Detection
import config_test

    
def main(list_buttons):
    """! Launch the RET
    @parameter list_buttons Once you chose what test you want to be running, the list_buttons will correspond to the button you are currently working with
    @return launch the whole test
    """
    try:
            # create an instance of Button_Pressing_Detection_Parameter
        parameter = Button_Pressing_Detection_parameter.RET_Parameter(list_buttons)
        parameter.define_measurement()
        if parameter.start_RET == False:
            print "The program is ended"
            return 0
        ## launch the daemon that process the information
        th_data_processing = Button_Pressing_Detection_data_processing.Rpi_data_processing_RET(parameter)
        th_data_processing.setDaemon(True)
        th_data_processing.start()
        for button in list_buttons:
            th_Button_Pressing_Detection = Button_Pressing_Detection.Btn_Pressing_Detection(parameter,button)
            th_Button_Pressing_Detection.start()
        # create an instance of Button_Pressing_Detection_Parameter_socket that hereditate from the Button_Pressing_Detection_Parameter
        #socket_server = Button_Pressing_Detection_socket.Rpi_SocketServer_RET(parameter)
        socket_client = Button_Pressing_Detection_socket.Rpi_SendMsg_Computer(parameter,button)
        
        for button in list_buttons:
            socket_client.Btn_send_information()
            
    except KeyboardInterrupt:
        config_test.stop_thread = True
    if config_test.stop_thread == True:
        return ("the test is over due to a stop_thread")
        quit()
             

if __name__ == "__main__":
    #test_running=raw_input("RET or BtnTesting?")
    #if test_running == "RET":
    list_buttons = config_test.list_two_buttons_RET
    #if test_running == "BtnTesting":
    #    list_buttons = config_test.list_one_button_testing
    main(list_buttons)
    
