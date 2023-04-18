import imp
from p2pclient import p2pclient
import json
import argparse
import sys
import time

if __name__ == "__main__":

    # parser = argparse.ArgumentParser(description = 'Access command line inputs')

    # parser.add_argument('-file', help='an integer for the accumulator')

    # args = parser.parse_args()

    print("client.py")

    file = open(sys.argv[2])
    json_file = json.load(file)


    client_id = json_file['client_id']
    content = json_file['content']
    actions = json_file['actions']
    print(client_id)

    ##############################################################################
    # You need to perform the following tasks:                                   #  
    # 1) Instantiate the client                                                  #
    # 2) Client needs to pick its serveport,bind to it                           #
    # 3) Register with bootstrapper                                              #
    # 4) STart listening on the port picked in step 2                            #
    # 5) Start executing its actions                                             #
    ##############################################################################

    #########################################################################################
    # TODO:  Read the client_id, content and actions from <file>.json, which you can obtain #
    #        from command line arguments. and feed it into the constructor of               #
    #        the p2pclient below                                                            #
    #########################################################################################
    #time.sleep(1)
    client = p2pclient(client_id=client_id, content=content, actions=actions)
    
    ##############################################################################
    # Now provided you have completed the steps in the p2pclient constructor     #
    # properly, steps                                                            #                  
    # 1, 2 and 3 are completed when you instantiate the client object            #  
    # We are left with steps 4 and 5                                             #
    ##############################################################################

    ##############################################################################
    # TODO: For step 4: call clients.start_listening()                           #
    ##############################################################################
    client.start_listening()

    ##############################################################################
    # For step 5: the bootstrapper will call the start() on this client, which  #
    # will make this client start taking its actions.                            #
    ##############################################################################