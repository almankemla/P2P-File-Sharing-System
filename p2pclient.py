"""
Follow the instructions in each method and complete the tasks. We have given most of the house-keeping variables
that you might require, feel free to add more if needed. Hints are provided in some places about what data types 
can be used, others are left to students' discretion, make sure that what you are returning from one method gets correctly
interpreted on the other end. Most functions ask you to create a log, this is important
as this is what the auto-grader will be looking for.
Follow the logging instructions carefully.
"""

"""
Appending to log: every time you have to add a log entry, create a new dictionary and append it to self.log. The dictionary formats for diff. cases are given below
Registraion: (R)
{
    "time": <time>,
    "text": "Client ID <client_id> registered"
}
Unregister: (U)
{
    "time": <time>,
    "text": "Unregistered"
}
Fetch content: (Q)
{
    "time": <time>,
    "text": "Obtained <content_id> from <IP>#<Port>
}
Purge: (P)
{
    "time": <time>,
    "text": "Removed <content_id>"
}
Obtain list of clients known to a client: (O)
{
    "time": <time>,
    "text": "Client <client_id>: <<client_id>, <IP>, <Port>>, <<client_id>, <IP>, <Port>>, ..., <<client_id>, <IP>, <Port>>"
}
Obtain list of content with a client: (M)
{
    "time": <time>,
    "text": "Client <client_id>: <content_id>, <content_id>, ..., <content_id>"
}
Obtain list of clients from Bootstrapper: (L)
{
    "time": <time>,
    "text": "Bootstrapper: <<client_id>, <IP>, <Port>>, <<client_id>, <IP>, <Port>>, ..., <<client_id>, <IP>, <Port>>"
}
"""
import socket
import time
from enum import Enum
import json
import random
import threading
import pickle
import struct

class Status(Enum):
            INITIAL = 0
            REGISTERED = 1
            UNREGISTERED = 2

class p2pclient:
    def __init__(self, client_id, content, actions):
        
        ##############################################################################
        # TODO: Initialize the class variables with the arguments coming             #
        #       into the constructor                                                 #
        ##############################################################################

        self.client_id = client_id
        self.content = content
        self.actions = actions  # this list of actions that the client needs to execute

        self.content_originator_list = None  # None for now, it will be built eventually
        self.log = []
        self.time = 0

        ##################################################################################
        # TODO:  You know that in a P2P architecture, each client acts as a client       #
        #        and the server. Now we need to setup the server socket of this client   #
        #        Initialize the the self.socket object on a random port, bind to the port#
        #        Refer to                                                                #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.         #
        ##################################################################################
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        random.seed(int(self.client_id))
        self.port = random.randint(9000, 9999)
        self.socket.bind(('127.0.0.1', self.port))
        


        ##############################################################################
        # TODO:  Register with the bootstrapper by calling the 'register' function   #
        #        Make sure you communicate to the B.S the serverport that this client#
        #        is running on to the bootstrapper.                                  #
        ##############################################################################
        self.status = Status.INITIAL
        self.register()
        

        
        
        ##############################################################################
        # TODO:  You can set status variable based on the status of the client:      #
        #        Registered: if registered to bootstrapper                           #
        #        Unregistered: unregistred from bootstrapper                         #
        #        Feel free to add more states if you need to                         #
        #        HINT: You may find enum datatype useful                             #
        ##############################################################################

        # 'log' variable is used to record the series of events that happen on the client
        # Empty list for now, update as we take actions
        # See instructions above on how to append to log
        

        # Timing variables:
        ###############################################################################################
        # TODO:  Ensure that you're doing actions according to time. B.S dictates time. Update this   #
        #        variable when BS sends a time increment signal                                       #
        ###############################################################################################
        


    def start_listening(self):
        ##############################################################################
        # TODO:  This function will make the client start listening on the randomly  #
        #        chosen server port. Refer to                                        #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        #        You will need to link each connecting client to a new thread (using #
        #        client_thread function below) to handle the requested action.       #
        ##############################################################################
        self.socket.listen()
        while True:
            (client_socket, address) = self.socket.accept()
            clientThread = threading.Thread(target = self.client_thread, args = (client_socket, address), daemon = True)
            clientThread.start()

    def client_thread(self, client_socket, address):
        ##############################################################################
        # TODO:  This function should handle the incoming connection requests from   #
        #        other clients.You are free to add more arguments to this function   #
        #        based your need                                                     #
        #        HINT: After reading the input from the buffer, you can decide what  #
        #        action needs to be done. For example, if the client is requesting   #
        #        list of known clients, you can return the output of self.return_list_of_known_clients #
        ##############################################################################
        
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                data_arr = data.split(" ")
                data = data_arr[1]
                ip = data_arr[2]
                port = data_arr[3]
                print("BS message received:" + data)
                
                if data == 'S':
                    self.start()
                elif data == 'K' :
                    client_list = self.return_list_of_known_clients() 
                    send = pickle.dumps(client_list)
                    client_socket.send(send.encode('utf-8'))
                elif data == 'CL' :
                    content_list = self.return_content_list()
                    send = pickle.dumps(content_list)
                    client_socket.send(send.encode('utf-8'))
                

    def register(self, ip = '127.0.0.1', port = 8888):
        ##############################################################################
        # TODO:  Register with the bootstrapper. Make sure you communicate the server#
        #        port that this client is running on to the bootstrapper.            #
        #        Append an entry to self.log that registration is successful         #
        ##############################################################################
        self.status = Status.REGISTERED
        bootstrapper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(2)
        bootstrapper_socket.connect((ip, port))

        send = str(str(self.client_id) + ' R '+ str(ip) +' '+str(self.port) + ' ' + str(self.status))
        print("Sending to BS:" + send)
        bootstrapper_socket.send(send.encode())
        
        bootstrapper_socket.close()
        self.log.append({"time" : self.time, "text" : str("Client ID " + str(self.client_id) + " registered")})
        string = "client_" + str(self.client_id) + ".json"
        with open(string, "w") as json_file:
            json.dump(self.log, json_file)



    def deregister(self, ip = '127.0.0.1', port = 8888):
        ##############################################################################
        # TODO:  Deregister/re-register with the bootstrapper                        #
        #        Append an entry to self.log that deregistration is successful       #
        ##############################################################################
        bootstrapper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(2)
        bootstrapper_socket.connect((ip, port))
        send = str(str(self.client_id) + ' U '+ str(ip) +' '+str(self.port) + ' ' + str(self.status))

        bootstrapperSocket.send(send.encode('utf-8'))
        bootstrapperSocket.close()

        self.log.append({"time" : self.time, "text" : str("Client ID " + str(self.client_id) +" deregistered")})
        string = "client_" + str(self.client_id) + ".json"
        with open(string, "w") as json_file:
            json.dump(self.log, json_file)


    def start(self):
        ##############################################################################
        # TODO:  When the Bootstrapper sends a start signal, the client starts       #
        #        executing its actions. Once this is called, you have to             #
        #        start reading the items in self.actions and start performing them   #
        #        sequentially, at the time they have been scheduled for, and as timed#
        #        by B.S. Once you complete an action, let the B.S know and wait for  #
        #        B.S's signal before continuing to next action                       #
        ##############################################################################
        #start = time.time()
        print("Start actions")
        #delay priority action k args 
        #sceh.scheduler
        
        
        #print("ACTION NUM: "+str(curr_act) + "CURR TIME " + str(curr_time))
        for action in self.actions:
            if self.time == action["time"]:
                print("CLIENT "+ str(self.client_id)+" ACTION NUM: "+ str(self.time) + " CODE: " + action["code"]+ " CURR TIME " + str(self.time))
                code = action["code"]
                if code == "R":#done
                    self.register()
                    print("register with bootstrapper")
                elif code == "U":#done
                    self.deregister()
                    print("deregister with bootstrapper")
                elif code == "Q":#done
                    self.request_content(action["content_id"])
                    print("request_content")
                elif code == "P":#done
                    self.purge_content(action["content_id"])
                    print("purge_content")
                elif code == "O":#done
                    self.query_client_for_known_client(action["client_id"], True)
                    print("query_client_for_known_client")
                elif code == "M":#done
                    self.query_client_for_content_list(action["client_id"], True)
                    print("query_client_for_content_list")
                elif code == "L":#done
                    self.query_bootstrapper_all_clients(True)
                    print("query_bootstrapper_all_clients")
                    #while_end = time.time()
                    #time.sleep(1.5 - (while_end-while_start) )
                    #create temp socket to send complete message

            
        # else:
        #     bootstrapper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     #time.sleep(2)
        #     bootstrapper_socket.connect(('127.0.0.1', 8888))
        #     send = str(str(self.client_id) + ' Complete '+ '127.0.0.1' +' '+str(self.port) + ' ' + str(self.status))
        #     bootstrapper_socket.send(send.encode('utf-8'))
        #     bootstrapper_socket.close()

        self.time += 1
        ##############################################################################
        # TODO:  ***IMPORTANT***                                                     #
        # At the end of your actions, “export” self.log to a file: client_x.json,    #
        # this is what the autograder is looking for. Python’s json package should   #
        # come handy.                                                                #
        ##############################################################################        
        

    #TODO: clarify on logging
    def query_bootstrapper_all_clients(self, log, ip = '127.0.0.1', port = 8888):
        ##############################################################################
        # TODO:  Use the connection to ask the bootstrapper for the list of clients  #
        #        registered clients.                                                 #
        #        Append an entry to self.log                                         #
        ##############################################################################
        print ("query_bootstrapper_all_clients")
        while self.status == Status.INITIAL:
            pass
        bootstrapper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #time.sleep(2)
        bootstrapper_socket.connect((ip, port))
        send = str(str(self.client_id) + ' AllClients '+ str(ip) +' '+str(self.port) + ' ' + str(self.status))

        bootstrapper_socket.send(send.encode('utf-8'))

        data = bootstrapper_socket.recv(1048).decode('utf-8')
        bootstrapper_socket.close()

        client_data_list = pickle.loads(data)
        new_data = ""
        for client in client_data_list:
            client_id, ip, port, status = client['client_id'], '127.0.0.1', client['port'], client['status']
            new_data += f'<{client_id}, {ip}, {port}>, '
        if log:
            self.log.append({"time": self.time, "text": str("Bootstrapper: " + new_data[: len(new_data) - 2])})
            string = "client_" + str(self.client_id) + ".json"
            with open(string, "w") as json_file:
                json.dump(self.log, json_file)

        return client_data_list
        

    #TODO: clarify on logging
    def query_client_for_known_client(self, client_id, log):
        client_list = None
        ##############################################################################
        # TODO:  Connect to the client and get the list of clients it knows          #
        #        Append an entry to self.log                                         #
        ##############################################################################
        actual_client = []
        bootstrapper_clients = self.query_bootstrapper_all_clients(log=False)
        for client in bootstrapper_clients:
            if client['client_id'] == client_id:
                actual_client = client
                break

        while self.status == Status.INITIAL:
            pass

        if len(actual_client) > 0:
            various_clients_sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(2)
            various_clients_sockets.connect((actual_client[1], int(actual_client[2])))
            send = str(str(self.client_id) + ' K '+ '127.0.0.1' +' '+str(self.port))

            various_clients_sockets.send(send.encode('utf-8'))

            data = various_clients_sockets.recv(1048).decode('utf-8')
            various_clients_sockets.close()

            client_list = pickle.loads(data)
            new_data = data.replace('[','<').replace(']','>').replace('\"','')
            new_data = new_data[1:len(new_data)-1]
            if log:
                self.log.append({"time": self.time, "text": str("Client " + str(client_id) + ": " + new_data)})
                string = "client_" + str(self.client_id) + ".json"
                with open(string, "w") as json_file:
                    json.dump(self.log, json_file)
        return client_list

    def return_list_of_known_clients(self):
        ##############################################################################
        # TODO:  Return the list of clients known to you                             #
        #        HINT: You can make a set of <client_id, IP, Port> from self.content_originator_list #
        #        and return it.                                                      #
        ##############################################################################
        known_clients = set()
        for content in self.content_originator_list:
            if self.client_id != int(self.content_originator_list[content][0]):
                known_clients.add((self.content_originator_list[content][0], self.content_originator_list[content][1], self.content_originator_list[content][2]))
        
        known_clients = [list(client) for client in known_clients]
        known_clients = sorted(known_clients, reverse=True)
        #change
        return [list(client) for client in known_clients]

    def query_client_for_content_list(self, client_id, log):
        content_list = None
        ##############################################################################
        # TODO:  Connect to the client and get the list of content it has            #
        #        Append an entry to self.log                                         #
        ##############################################################################
        actual_client = []

        bootstrapper_clients = self.query_bootstrapper_all_clients(log = False)
        for client in bootstrapper_clients:
            if client[0] == client_id:
                print("~~~~~client: "+str(self.client_id) + " " +str(client[0]) + " " + client[1] + " " + str(client[2]))
                actual_client = client
                break

        while self.status == Status.INITIAL:
            pass
        if len(actual_client) > 0:
            various_clients_sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            time.sleep(2)
            various_clients_sockets.connect((actual_client[1], int(actual_client[2])))
            send = str(str(self.client_id) + ' CL '+ '127.0.0.1' +' '+str(self.port))
            various_clients_sockets.send(send.encode('utf-8'))

            data = various_clients_sockets.recv(1048).decode('utf-8')
            various_clients_sockets.close()
            print("~~~~~~~~~~~content list from client: "+str(client_id)+ " "+data)
            content_list = picle.loads(data)
            new_data = data.replace('[','<').replace(']','>').replace('\"','')
            new_data = new_data[1:len(new_data)-1]
            if log:
                self.log.append({"time": self.time, "text": "Client " + str(client_id) + ": " + new_data})
                string = "client_" + str(self.client_id) + ".json"
                with open(string, "w") as json_file:
                    json.dump(self.log, json_file)

        return content_list


    def return_content_list(self):
        ##############################################################################
        # TODO:  Return the content list that you have (self.content)                #
        ##############################################################################
        return self.content

    def request_content(self, content_id):
        #####################################################################################################
        # TODO:  Your task is to obtain the content and append it to the                                    #
        #        self.content list.  To do this:                                                            #
        #        Get the content as per the instructions in the pdf. You can use the above query_*          #
        #        methods to help you in fetching the content.                                               #
        #        Make sure that when you are querying different clients for the content you want, you record#
        #        their responses(hints, if present) appropriately in the self.content_originator_list       #
        #        Append an entry to self.log that content is obtained                                       #
        #####################################################################################################

        found_content_client = [None, None, None]
        bootstrapper_clients = self.query_bootstrapper_all_clients(log = False)
        index = 0
        hint = 0
        found = False
        count = 0   

        list_of_ids = [i[0] for i in bootstrapper_clients]

        print("~~~~~list of ids "+pickle.dumps(list_of_ids))
        while not found and index < len(bootstrapper_clients) and count < 10:
            print("~~~~~Client index "+str(index) + " " + str(len(bootstrapper_clients)))
            client = bootstrapper_clients[index]
            print("~~~~~Client: "+str(self.client_id)+" Looking at client: "+str(client[0]))
            if client[0] != self.client_id:
                content_list = self.query_client_for_content_list(client[0], log=False)
                if not content_list:
                    print("~~~~~content list is empty "+ str(client[0]))
                    break
                in_list = False
                in_col = None
                for content in content_list:
                    self.content_originator_list[content] = [client[0], client[1], client[2]]
                    if content == content_id:
                        found_content_client = [client[0], client[1], client[2]]
                        found = True
                        in_list = True
                        break
                if not in_list:
                    if content_id in self.content_originator_list:
                        in_col = self.content_originator_list[content_id]
                        hint = in_col[0]
                        print("~~~~~found hint at client_id "+str(hint))
                        index = list_of_ids.index(hint)
                    else:
                        index += 1
                else:
                    index += 1
                count += 1

        self.content.append(content_id)

        q_dict["text"] = str("Obtained "+str(content_id)+" from " + found_content_client[1] + "#" + found_content_client[2])
        self.log.append({"time": self.time, "text": str("Obtained "+ str(content_id) +" from " + found_content_client[1] + "#" + found_content_client[2])})
        string = "client_" + str(self.client_id) + ".json"
        with open(string, "w") as json_file:
            json.dump(self.log, json_file)

    def purge_content(self, content_id):
        #####################################################################################################
        # TODO:  Delete the content from your content list                                                  #
        #        Append an entry to self.log that content is purged                                         #
        #####################################################################################################
        self.content.remove(content_id)
        self.log.append({"time": self.time, "text": str("Removed "+ str(content_id))})
        string = "client_" + str(self.client_id) + ".json"
        with open(string, "w") as json_file:
            json.dump(self.log, json_file)
