from socket import *
import json


class HOAStryngC:
    # <start of class>
    DELIM = "~~~~~~()"
    PROTOCOL_HEADER = "HOAS/1.0 "

    # funtions

    def __init__(self, hostName, portNumber):
        self.__prepSocket(hostName, portNumber)

    # set up socket 
    def __prepSocket(self, hostName, portNumber):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((hostName, portNumber))        
        # end of prepSocket


    # send though server socket
    def __sendToSocket(self, packet):
        self.clientSocket.send(packet.encode())
        #end of sendToSocket


    # blocking read from the socket 
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
            print("here HCS rfs 7")

        return packet
        #end of recieveFromSocket


    def __processReturnedInfo(self, response):
        # first space is the end of the protocol header
        hdr = response.split(" ", 1)
        
        # next space is the end of the statusCode
        # get status code
        statC = hdr[1].split(" ",1)

        # then new line is the end of the status message
        statusMsg = statC[1].split("\n", 1)

        # get data 
        
        dataAndDelim = statusMsg[1]
        print(dataAndDelim)
        #data = dataAndDelim[1].split(self.DELIM, 1)
        data = dataAndDelim.split(self.DELIM,1)
        print("data(" + data[0] + ")")

        print("here HCS" + data[0])
        # if there was data 
        if len(data[0]) != 0 :
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
        


    # register
    def register(self, username):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "REGI\n" + username + self.DELIM
        print("here HCS - 3")
        # send the packet
        self.__sendToSocket(packet)
        print("here HCS - 4")
        
        # read response from server
        response = self.__recieveFromSocket()
        print("here HCS - 5")
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end of register


    # request list of games
    def requestGamesList(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "LIST\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end of requestGamesList
    

    # create a new game
    def createNewGame(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "CREA\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end of createNewGame


    # join a game 
    def joinGame(self, gameID):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "JOIN\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end join game


    # exit the game
    def exitGame(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "EXIT\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end exitGame


    # unregister 
    def unregister(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "UNRG\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end unregister


    # guess letter
    def guessLetter(self, guessedLetter):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "GUEL\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        # end guessLetter


    #NOTE, not necessary, complete this later
    # guess word (optional)
    def __guessWord(self, guessedWord):
        # build the packet using our protocol 
        print("delete this later")
        #end guessWord


    # select a word
    def selectWord(self, enteredWord):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "SLWD\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        #end selectWord


    # initialize guesser 
    def initGuesser(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "INIG\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        #end initGuesser


    # ask game state
    def askGameState(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "AKGS\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        #end askGameState


    # get my points
    def getMyPoints(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "GMPT\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        #end getMyPoints


    # get opponent's points
    def getOpponentPoints(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "GOPT\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)


    ## NOTE, EC, complete this later...
    # get scoreboard
    def getScoreboard(self):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "GTSB\n" + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()
        # process the returned packet and send back a return dict
        return self.__processReturnedInfo(response)
        #end getScoreboard


    # <end of class>

