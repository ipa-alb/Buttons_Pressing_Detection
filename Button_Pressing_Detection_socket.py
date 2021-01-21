#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:52:41 2021

@author: ubuntu
"""

import socket,sys,threading
import config
import Button_Pressing_Detection_parameter as RET_Param

class Rpi_ReceiveMsg_Computer(threading.Thread):
    def __init__(self, connection,client_connection,parameter):
        threading.Thread.__init__(self)
        self.connection = connection
        self.conn_client = client_connection ## put it as a attribute of the thread
        self.list_msg=[]
        self.parameter = parameter
        


        
    def run(self):
        nom = self.getName() 
        while config.stop_thread == False:
            msgClient = self.connection.recv(1024)
            if msgClient.upper() == "END" or msgClient =="":
                break
            message = "%s" %(msgClient)
            print "*" + msgClient + "*"
            try :
                self.list_msg = msgClient.split(";")
                if self.list_msg[2]=='enter': # knowing in which phase we are
                    #I am logging the whole message in order to process the time comparison during the time_interval the robot is moving from Btn1 to Btn2
                    self.parameter.list_msg_entering_Btn_area = self.list_msg
                if self.list_msg[2]=='leave':
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
    def __init__(self,connection,parameter):
        threading.Thread.__init__(self)
        self.connection = connection
        self.parameter = parameter
        self.msg = "pressed"
        
    def run(self):
        while config.stop_thread == False:
            for button in self.parameter.list_buttons:
                if button.Btn_send_information == True:
                    self.connection.send(str(self.parameter.time_Btn_Pressed)+";"+button.Btn_name+";"+self.msg)
                    button.Btn_send_information = False




class Rpi_SocketServer_RET(RET_Param.RET_Parameter):
    def __init__(self,parameter):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.mySocket.bind((parameter.socket_host, parameter.socket_port))
        except socket.error:
            print "The link with the chosen address socket failed."
            sys.exit()
        print "Servor ready, waiting for answer.."
        self.mySocket.listen(5)
        while config.stop_thread == False:
            connection, address = self.mySocket.accept()# Accept the connection of client
            client_connection = {}
            th_Rpi_ReceiveMsg_Computer = Rpi_ReceiveMsg_Computer(connection,client_connection,parameter)
            th_Rpi_ReceiveMsg_Computer.setDaemon(True)
            th_Rpi_ReceiveMsg_Computer.start()
            th_Rpi_SendMsg_Computer = Rpi_SendMsg_Computer(connection,parameter)
            th_Rpi_SendMsg_Computer.setDaemon(True)
            th_Rpi_SendMsg_Computer.start()
            # Dialogue avec le client :
            connection.send("You are connected. Send your message.")


    



                

