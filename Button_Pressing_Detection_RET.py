#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:51:34 2021

@author: ubuntu
"""

import Button_Pressing_Detection_parameter
import Button_Pressing_Detection_socket 
import Button_Pressing_Detection_data_processing
import Button_Pressing_Detection
import config_test

    
def main(list_buttons):
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
        socket_server = Button_Pressing_Detection_socket.Rpi_SocketServer_RET(parameter)
    except KeyboardInterrupt:
        config_test.stop_thread = True

             

if __name__ == "__main__":
    test_running=raw_input("RET or BtnTesting?")
    if test_running == "RET":
        list_buttons = config_test.list_two_buttons_RET
    if test_running == "BtnTesting":
        list_buttons = config_test.list_one_button_testing
    main(list_buttons)
    
