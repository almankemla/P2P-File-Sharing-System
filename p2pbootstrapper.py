"""
Follow the instructions in each method and complete the tasks. We have given most of the house-keeping variables
that you might require, feel free to add more if needed. Hints are provided in some places about what data types 
can be used, others are left to user discretion, make sure that what you are returning from one method gets correctly
interpreted on the other end. 
"""
import socket
import threading
import sys
import time
import pickle
import json
from enum import Enum
import random
from p2pclient import Status

class p2pbootstrapper:
    def __init__(self, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Initialize the socket object and bind it to the IP and port, refer  #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        ##############################################################################
        
        
        self.time = 0
        self.MAX_CLIENTS = 20
        self.boots_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boots_socket.bind((ip, port))
        self.clients = []  # None for now, will get updates as clients register

        # Append the log to this variable.
        self.log = []
        self.action = 0
        


        # Timing variables:
        ###############################################################################################
        # TODO:  To track the time for all clients, self.time starts at 0, when all clients register  #
        #        self.MAX_CLIENTS is the number of clients we will be spinnign up. You can use this   #
        #        to keep track of how many 'complete' messages to get before incrementing time.       #
        #        CHange this when testing locally                                                     #
        ###############################################################################################
                


    def start_listening(self):
        ##############################################################################
        # TODO:  This function will make the BS start listening on the port 8888     #
        #        Refer to                                                            #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        #        You will need to link each connecting client to a new thread (using #
        #        client_thread function below) to handle the requested action.       #
        ##############################################################################
        
        self.boots_socket.listen(self.MAX_CLIENTS)
        while True:
            (client_socket, address) = self.boots_socket.accept()

            clientThread = threading.Thread(target = self.client_thread, args = (client_socket, ), daemon = True)
            clientThread.start()

    def client_thread(self, client_socket):
        ##############################################################################
        # TODO:  This function should handle the incoming connection requests from   #
        #        clients. You are free to add more arguments to this function based  #
        #        on your need                                                        #
        #        HINT: After reading the input from the buffer, you can decide what  #
        #        action needs to be done. For example, if the client wants to        #
        #        deregister, call self.deregister_client                             #
        ##############################################################################

        while True :
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

            if data:
                data_arr = data.split()
                client_id = data_arr[0]
                data = data_arr[1]
                ip = data_arr[2]
                port = data_arr[3]
                status = data_arr[4]

                if data == 'U' :
                    self.deregister_client(client_id, ip, port, status)
                    self.process_action_complete()
                elif data == 'R' :
                    self.register_client(client_id, ip, port, status)
                    self.process_action_complete()
                # elif data == 'S':
                #     self.start()
                #     print("start complete for " + str(client_socket))
                elif data == 'Complete':
                    print(client_id + " has completed")
                    self.process_action_complete()
                    return
                elif data == 'AllClients':
                    client_list = self.return_clients()
                    sorted_list = sorted(client_list, key=lambda x: x[0]) 
                    send = pickle.dumps(sorted_list)

                    client_socket.send(send.encode('utf-8'))
            
            

                     

    def register_client(self, client_id, ip, port, status):  
        ##############################################################################
        # TODO:  Add client to self.clients                                          #
        ##############################################################################

        print("Bootstrapper register client " + str(client_id))
        self.clients.append({"client_id": client_id, "ip": ip, "port": port, "status": status})

    def deregister_client(self, client_id, ip, port, status):
        ##############################################################################
        # TODO:  Delete client from self.clients                                     #
        ##############################################################################
        print("Bootstrapper deregister client " + str(client_id))
        self.clients.remove({"client_id": client_id, "ip": ip, "port": port, "status": status})

    def return_clients(self):
        ##############################################################################
        # TODO:  Return self.clients                                                 #
        ##############################################################################
        print("Bootstrapper return clients")
        return self.clients

    def start(self):
        ##############################################################################
        # TODO:  Start timer for all clients so clients can start performing their   #
        #        actions                                                             #
        ##############################################################################
        print("Bootstrapper start")
        if(self.time==7):
            return 
        self.time += 1
        print("BS time: " + str(self.time))
        for client in self.clients:
            start_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            start_client_socket.connect(('127.0.0.1', int(client['port'])))

            send = str(client['client_id'] + ' S '+ '127.0.0.1' +' '+ str(8888))
            start_client_socket.send(send.encode('utf-8'))

            start_client_socket.close()

    def process_action_complete(self):
        ##############################################################################
        # TODO:  Process the 'action complete' message from a client,update time if  #
        #        all clients are done, inform all clients about time increment       #
        ##############################################################################
        
        clients_text = ""
        self.action += 1

        print("process_action_complete, action: " + str(self.action))
        if self.action == self.MAX_CLIENTS:
            path = 'bootstrapper.json'
            self.action = 0
            print(self.clients)

            for client in self.clients:

                print("ID: " + client['client_id'] + " time: " + str(self.time))
                client_id, ip, port, status = client['client_id'], '127.0.0.1', client['port'], client['status']
                if status == Status.REGISTERED:
                    print("adding:" + client['client_id'])
                    clients_text += f'<{client_id}, {ip}, {port}>, '
            self.log.append({"time": self.time, "text": "Clients registered: " + clients_text[: len(clients_text) - 2]})
            print(self.log)
            with open(path, "w") as json_file:
                json.dump(self.log, json_file)
            self.start()
            
            

        
                       
            