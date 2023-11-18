from socket import *
import select
import random
import json



class HOAStryngS:
    DELIM = "~~~~~~()"
    PROTOCOL_HEADER = "HOAS/1.0 "
    ACCEPTED_METHOD_TYPES = {"REGI", "LIST", "CREA", "JOIN", "EXIT", "UNRG", "GUEL", "SLWD", "INIG", "AKGS", "GTMP", "GOPT", "GTSB" }


    def __init__(self, serverPort):
        self.activeClientConnections = dict()
        self.__prepListener(serverPort)
        # end init


    # prep listener
    def __prepListener(self, serverPort: int):
        self.serverListenerSock = socket(AF_INET, SOCK_STREAM)
        self.serverListenerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverListenerSock.bind(('', serverPort))
        self.serverListenerSock.listen(1)
        #end prepListener


    def __sendToSocket(self, clientID, packet):
        # send the packet to the proper client connection
        self.activeClientConnections[clientID].send(packet.encode())      
        #end of sendToSocket


    # does a non blocking read on the given connectionSocket
    # returns the packet read, or none if the connection
    # has not sent anything to this socket
    def __nonBlockingRecieveFrom(self, connectionSocket):
        # the connectionSocket was set to non-blocking earlier
        connectionSocket.setblocking(0)
        packet = connectionSocket.recv(1024).decode()

        # if connection didnt send anything return none
        if len(packet) == 0:
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


    def __parseRequestPacket(self, packet):
        #Protocol_header + method_type + "\n" + requestData + delim
        
        # first space is the end of the protocol header
        hdr = packet.split(" ", 1)
        
        # next \n is the end of the statusCode
        # get status code
        methodType = hdr[1].split("\n", 1)

        # then delim is the end of the data
        data = methodType[1].split(self.DELIM,1)
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
        # generate random # [0,9999]
        tempID = random.randrange(0, 9999, 1)

        while(tempID in self.activeClientConnections.keys()):
            #while tempIDis one of the keys, keep trying
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

        if packet is None:
            return
        
        # first 8 Bytes is the PROTOCOL_HEADER
        # find the next 4 bytes of the packet determine the method type
        #methodType = packet[8 : 12] #[8,11]
        hdr = packet.split(" ", 1)
        methodType = hdr[1].split("\n",1)

        #methodType[0] is method Type
        if methodType[0] not in self.ACCEPTED_METHOD_TYPES:
            self.__sendToSocket((self.PROTOCOL_HEADER + "40 " + "Invalid Method Type\n" + self.DELIM))
            return None; 

        # call parser to parse the packet 
        return self.__parseRequestPacket(packet)
        #end of pollClientForRequest


    def sendDataToClient(self, clientID,  statusCode: str="20", statusMessage="OK", data=None):
        if (data is not None):
            jsonDumpedData = json.dumps(data)
            packet = self.PROTOCOL_HEADER + statusCode + " " + statusMessage + "\n" + jsonDumpedData + self.DELIM
        else:
            packet = self.PROTOCOL_HEADER + statusCode + " " + statusMessage + "\n" + self.DELIM
        self.__sendToSocket(clientID, packet)
        #end of sendDataToClient


    def removeClient(self, clientID):
        self.activeClientConnections[clientID].close()
        del self.activeClientConnections[clientID]
        #end removeClient


        
    #end HOAStryngS