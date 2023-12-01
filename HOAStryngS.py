from socket import *
import select
import random
import json

"""
Hangman - Term Project
with Hanging on a Stryng protocol
authors : Jeffrey Caruso, Cordelia Notbohm
date    : Fall 2023
file    : HOAStryngS.py
class   : HOAStryngS
"""

# a class that handles the server side of the HOAS protocol 
class HOAStryngS:
    DELIM = "~~~~~~()"
    PROTOCOL_HEADER = "HOAS/1.0 "
    ACCEPTED_METHOD_TYPES = {"REGI", "LIST", "CREA", "JOIN", "EXIT", "UNRG", "GUEL", "SLWD", "AKGS", "GTSB" }


    def __init__(self, serverPort):
        self.activeClientConnections = dict()
        self.__prepListener(serverPort)
        # end init


    # prep listener socket
    def __prepListener(self, serverPort: int):
        # IP , TCP
        self.serverListenerSock = socket(AF_INET, SOCK_STREAM)
        # don't hold the server socket after app close
        self.serverListenerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #bind server port while app is running
        self.serverListenerSock.bind(('', serverPort))
        #set to be listening
        self.serverListenerSock.listen(1)
        #end prepListener


    # send a packet though the correct conection socket
    def __sendToSocket(self, clientID, packet):
        print("Sent message to: " + str(clientID))
        self.activeClientConnections[clientID].send(packet.encode())      
        #end of sendToSocket


    # does a non blocking read on the given connectionSocket
    # returns the packet read, or none if the connection
    # has not sent anything to this socket
    def __nonBlockingRecieveFrom(self, connectionSocket):
        # set the connectionSocket to non-blocking
        connectionSocket.setblocking(0)

        packet = ""
        try:
            packet = connectionSocket.recv(1024).decode()
        except:
            #if there was nothing to recieve
            packet = ""
            

        # if connection didnt send anything return none
        if len(packet) == 0:
            connectionSocket.setblocking(1)
            return None

        # while we have yet to get the end of the packet
        # (haven't found the delimiter)
        # we don't need to check if there is something after the 
        # delimiter becuase in our protocol the client would not
        # be sending two packets in a row, it waits for a response
        # before issuing another request 
        while packet.find(self.DELIM) == -1:
            packet += connectionSocket.recv(1024).decode()

        connectionSocket.setblocking(1)
        return packet
        #end of __nonBlockingRecieveFrom


    # turn a request packet into an easy to use dictornary that
    # abstracts away the protocol
    def __parseRequestPacket(self, packet):
        #Protocol_header + " " +  method_type + "\n" + request_data + delimiter 
        
        # first space is the end of the protocol header
        hdr = packet.split(" ", 1)
        
        # get method type
        methodType = hdr[1].split("\n", 1)

        # delim is at the end of the data
        # get data
        data = methodType[1].split(self.DELIM,1)

        # format the packet into a dictionary
        if len(data[0]) > 0 :
            returnDict = {
                "Method Type" : methodType[0],
                "Data" : data[0]
            }
            return returnDict
        else:
            returnDict = {
                "Method Type" : methodType[0]
            }
            return returnDict
        #end of __parseRequestPacket
    

    # generates a new unique four digit client ID number
    def __getNewClientID(self):
        # generate random #
        tempID = random.randrange(0, 9999, 1)

        while(tempID in self.activeClientConnections.keys()):
            # Keep trying to get a unique ID
            tempID = random.randrange(0, 9999, 1)
            
        return tempID
        #end __createNewClientID


    # polls for any new client connection by doing a 
    # non-blocking accept on the lister Socket
    # return the new clientID or -1 if no new clients were found
    def pollForNewClientConnection(self):
        # check if the listener socket has anything to read
        read_list = [self.serverListenerSock]
        readable, writable, errored = select.select(read_list, [], [], 0.1)

        # if socket does have something to read, accept a new client connection
        for s in readable:
            if s is self.serverListenerSock:
                #have a connection to make, so make a connection on a new socket
                connectionSocket, clientAddress = self.serverListenerSock.accept()
                # add generate unique ID and add connection to list of active clients
                clientID = self.__getNewClientID()
                self.activeClientConnections[clientID] = connectionSocket
                return clientID
        # if socket does not have something to read, return -1  
        return -1
        #end of pollForNewClientConnection
        


    # poll for client request
    # return tuple with first value being method type, and the rest being the parameters 
    # that the client sent with that method.
    def pollClientForRequest(self, clientID):
        # see if socket has anything to read
        clientConnection = self.activeClientConnections[clientID]
        packet = self.__nonBlockingRecieveFrom(clientConnection)

        # if no packet, stop processing
        if packet is None:
            return
        
        # first is the PROTOCOL_HEADER
        # next is 4 characters identifying the method type
        hdr = packet.split(" ", 1)
        methodType = hdr[1].split("\n",1)

        #methodType[0] is method Type
        if methodType[0] not in self.ACCEPTED_METHOD_TYPES:
            packet = self.PROTOCOL_HEADER + "40 " + "Invalid Method Type\n" + self.DELIM
            self.__sendToSocket(clientID, packet)
            return None; 

        # call parser to parse the packet 
        return self.__parseRequestPacket(packet)
        #end of pollClientForRequest


    # creates a packet using the protocol with the given data inside, and 
    # sends it to the client
    def sendDataToClient(self, clientID,  statusCode: str="20", statusMessage="OK", data=None):
        if (data is not None):
            #take data structures dump into a stream that can be sent on network
            jsonDumpedData = json.dumps(data)
            packet = self.PROTOCOL_HEADER + statusCode + " " + statusMessage + "\n" + jsonDumpedData + self.DELIM
        else:
            packet = self.PROTOCOL_HEADER + statusCode + " " + statusMessage + "\n" + self.DELIM
        #send it
        self.__sendToSocket(clientID, packet)
        #end of sendDataToClient


    # remove all connection data for a client
    def removeClient(self, clientID):
        self.activeClientConnections[clientID].close()
        del self.activeClientConnections[clientID]
        #end removeClient

    #end HOAStryngS