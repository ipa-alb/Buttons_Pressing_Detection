#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:52:41 2021

@author: ubuntu
"""


#@file Button_Pressing_Detection_socket.py
#@section RET_communication Description
# The RET_communication application is made of 3 class. The first class is the Rpi_SocketServer_RET that insure the opening of the socket server that is gonna
#be efficient during the RET. Moreover the creation of an instance of the Rpi_SocketServer_RET object initialize two threads, from each class. 
# We are defining the thread communication as daemon on the Rpi, because the main event to be detected is the Button Pressing, and we do not want anything 
# to interfere with that information.
#@section libraries_Button_Pressing_Detection_socket Libraries/modules
# Custom class:
#   - Button_Pressing_Detection_parameter
#   - config_test
# Standard library:
#   - socket
#   - sys
#   - threading
#@section todo_RET_Communication
# Improve the closing of the communication when the RET is over. The thread are easily stopped, however we are killing the socket, instead of closing it properly.

import socket,sys,threading
import config_test
import Button_Pressing_Detection_parameter as RET_Param

class Rpi_ReceiveMsg_Computer(threading.Thread):
    """! The Rpi_ReceiveMsg_Computer base class.
    Defines the thread that is receiveing message from the computer
    """
    def __init__(self, connection,client_connection,parameter):
        """! The Rpi_ReceiveMsg_Computer class initializer
        @param connection the connection to the socket opened between the Rpi and the computer
        @param client_connection the connection to the client_sender on the computer
        @param parameter the parameter that the Btn_Pressing_Detection has to deal with
        @return a thread that receives the message from the computer 
        """
        threading.Thread.__init__(self)
        self.connection = connection
        self.conn_client = client_connection ## put it as a attribute of the thread
        self.list_msg=[]
        self.parameter = parameter
        


        
    def run(self):
        """! The Rpi_ReceiveMsg_Computer run
        @return a loop for the thread to run in or stop the test when the time of the test is completed
        When we received the message that the end effector is entering or leaving the button area, we log it
        We have add an exit to the whole application if the Rpi receive a stop message. We can then stop the test from the computer
        """
        nom = self.getName() 
        while config_test.stop_thread == False:
            msgClient = self.connection.recv(1024)
            if msgClient.upper() == "STOP" or msgClient =="":
                config_test.stop_thread = True
                break
            message = "%s" %(msgClient)
            print "*" + msgClient + "*"
            try :
                self.list_msg = msgClient.split(";")
                if self.list_msg[2]=='entering': # knowing in which phase we are
                    #I am logging the whole message in order to process the time comparison during the time_interval the robot is moving from Btn1 to Btn2
                    self.parameter.list_msg_entering_Btn_area = self.list_msg
                if self.list_msg[2]=='leaving':
                    self.parameter.list_msg_leaving_Btn_area = self.list_msg
                    #LAUNCH THE DATA PROCESSING
                    self.parameter.process_information = True
                    ######
                # Close the connection :
            except:
                pass
            for cle in self.conn_client:
                if cle != nom:      # do not send it back to the one who emit it
                    self.conn_client[cle].send(message)
        self.connection.close()      # cut connexion from the server with client
#        del self.conn_client[nom]        # suppress his entrance from the dictionnary
        print "Client %s disconnected." % nom
        # The thread is done here   

class Rpi_SendMsg_Computer(threading.Thread):
    """! The Rpi_SendMsg_Computer base class.
    Defines the thread that is sending message to the computer
    """
    def __init__(self,connection,parameter):
        """! The Rpi_SendMsg_Computer class initializer
        @param connection the connection to the socket opened between the Rpi and the computer
        @param parameter the parameter that the Btn_Pressing_Detection has to deal with
        @return a thread that send the messages to the computer 
        """
        threading.Thread.__init__(self)
        self.connection = connection
        self.parameter = parameter
        
    def run(self):
        """! The Rpi_SendMsg_Computer run
        @return a loop for the thread to run in or stop the test when the time of the test is completed
        When a button is pressed, we send it to the computer
        """
        while config_test.stop_thread == False:
            for button in self.parameter.list_buttons:
                if button.Btn_send_information == True:
                    print("I am sending this info")
                    self.connection.send(str(self.parameter.time_Btn_change_state)+";"+button.Btn_name+";"+self.parameter.Btn_state)
                    button.Btn_send_information = False




class Rpi_SocketServer_RET(RET_Param.RET_Parameter):
    def __init__(self,parameter):
        """! The Rpi_SocketServer_RET class initializer
        @param parameter the parameter that the Btn_Pressing_Detection has to deal with
        @return a socket connection and launch the thread that are communicating with the computer 
        """
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.mySocket.connect((parameter.socket_host, parameter.socket_port))
        except socket.error:
            print "The link with the chosen address socket failed."
            print(parameter.socket_host)
            print( parameter.socket_port)
            sys.exit()
            quit()
        print "Servor ready, waiting for answer.."
        self.mySocket.listen(5)
        connection, address = self.mySocket.accept()# Accept the connection of client
        client_connection = {}
        th_Rpi_ReceiveMsg_Computer = Rpi_ReceiveMsg_Computer(connection,client_connection,parameter)
        #define the communication as a daemon for it not to interfere with the button pressing detection
        th_Rpi_ReceiveMsg_Computer.setDaemon(True)
        th_Rpi_ReceiveMsg_Computer.start()
        th_Rpi_SendMsg_Computer = Rpi_SendMsg_Computer(connection,parameter)
        th_Rpi_SendMsg_Computer.setDaemon(True)
        th_Rpi_SendMsg_Computer.start()
        # Dialogue avec le client :
        connection.send("You are connected. Send your message.")


    



                

