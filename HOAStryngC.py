from socket import *
import json

"""
Hangman - Term Project
with Hanging on a Stryng protocol
authors : Jeffrey Caruso, Cordelia Notbohm
date    : Fall 2023
file    : HOAStryngC.py
class   : HOAStryngC
"""

# a class that handles the client side of the HOAS protocol 
class HOAStryngC:
    DELIM = "~~~~~~()"
    PROTOCOL_HEADER = "HOAS/1.0 "

    def __init__(self):
        init = True
        #end init

    # set up connection socket 
    def __prepSocket(self, hostName, portNumber):
        # IP , TCP
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((hostName, portNumber))        
        # end of prepSocket


    # send though connection socket
    def __sendToSocket(self, packet):
        self.clientSocket.send(packet.encode())
        #end of sendToSocket


    # blocking read from the connection socket 
    def __recieveFromSocket(self):
        bytePacket = self.clientSocket.recv(1024)
        packet = bytePacket.decode()

        # while we have yet to get the end of the packet
        # (haven't found the delimiter)
        # we don't need to check if there is something after the 
        # delimiter becuase in our protocol the client would not
        # be sending two packets in a row, it waits for a response
        # before issuing another request 
        while packet.find(self.DELIM) == -1:  
            bytePacket = self.clientSocket.recv(1024)
            packet += bytePacket.decode()
            print("waiting on server (ctrl + c to give up)")

        return packet
        #end of recieveFromSocket


    # turn a response packet into am easy to use dictornary that
    # abstracts away the protocol
    def __processReturnedInfo(self, response):
        # Protocol_header + " " + status_code + " " 
        # + Status_message + "\n" + data_requested + delimiter 

        # first space is the end of the protocol header
        hdr = response.split(" ", 1)
        
        # get status code
        statC = hdr[1].split(" ",1)

        # then new line is the end of the status message
        statusMsg = statC[1].split("\n", 1)

        # get data 
        dataAndDelim = statusMsg[1]
        data = dataAndDelim.split(self.DELIM,1)

        # if there was data 
        if len(data[0]) != 0 :
            #unloading data from net into desired structure
            data_loaded = json.loads(data[0])
            returnDict = {
                "Status Code" : statC[0],
                "Status Message" : statusMsg[0],
                "Data" : data_loaded
            }
            return returnDict
        
        # if there was no data 
        else:
            returnDict = {
                "Status Code" : statC[0],
                "Status Message" : statusMsg[0]
            }
            return returnDict
        #end processReturnedInfo
        

    # send a constructed request packet, wait for a response
    # and then return a dic with a processsed return
    def __sendRequestAndReturnResponse(self, packet):
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        #end of __sendRequestAndReturnResponse


    # register with a server
    def register(self, hostName, portNumber, username):
        self.__prepSocket(hostName, portNumber)
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "REGI\n" + username + self.DELIM
        # send the packet and return result 
        response =  self.__sendRequestAndReturnResponse(packet)
        if response["Status Code"] != "20":
            print("bad response!")
            self.clientSocket.close()

        return response
        # end of register


    # request list of games from a server
    def requestGamesList(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "LIST\n" + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        # end of requestGamesList
    

    # create a new game
    def createNewGame(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "CREA\n" + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        # end of createNewGame


    # join a game 
    def joinGame(self, gameID):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "JOIN\n" + str(gameID) + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        # end join game


    # exit the game
    def exitGame(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "EXIT\n" + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        # end exitGame


    # unregister from a server
    def unregister(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "UNRG\n" + self.DELIM
        # send the packet and get response
        response =  self.__sendRequestAndReturnResponse(packet)
        # close the socket 
        self.clientSocket.close()
        # return the socket
        return response
        # end unregister


    # guess letter
    def guessLetter(self, guessedLetter):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "GUEL\n" + guessedLetter + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        # end guessLetter


    # select a word
    def selectWord(self, enteredWord):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "SLWD\n" + enteredWord + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        #end selectWord


    # ask game state
    def askGameState(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "AKGS\n" + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        #end askGameState


    # get scoreboard
    def getScoreboard(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "GTSB\n" + self.DELIM
        # send the packet and return result 
        return self.__sendRequestAndReturnResponse(packet)
        #end getScoreboard

    # end of HOAStryngC

