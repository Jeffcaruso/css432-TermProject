from socket import *


class HOAStryngC:
    # <start of class>
    DELIM = "~~~~~~()"
    PROTOCOL_HEADER = "HOAS/1.0 "

    # funtions

    def __init__(self, portNumber, hostName):
        self.__prepSocket(portNumber, hostName)

    # set up socket 
    def __prepSocket(self, portNumber, hostName):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((hostName, portNumber))        
        # end of prepSocket


    # send though server socket
    def __sendToSocket(self, packet):
        self.clientSocket.send(packet)
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
            packet += bytePacket.decode

        return packet
        #end of recieveFromSocket

    # register
    def register(self, hostName, portNumber, username):
        # build the packet using our protocol 
        packet = self.PROTOCOL_HEADER + "REGI" + username + self.DELIM
        # send the packet
        self.__sendToSocket(packet)
        # read response from server
        response = self.__recieveFromSocket()

        # first 8 bytes are protocol header

        # next two bytes are register status
        status = response[8:10]##[8,10) 

        # anything after that and before the delimiter is error message
        if status == "OK":
            print(test)

        return (registrationStatus, reponseCode)

        # return bool for success or failure?
        # end of register

    # request list of games
    def requestGamesList(self):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet
        
        # return list of games
        # end of requestGamesList

    # create a new game
    def createNewGame(self):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet
      
        # return the game ID of new game
        # end of createNewGame

    # join a game 
    def joinGame(self, gameID):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet
        # return if you are "starting first" 
        # end join game

    # exit the game
    def exitGame(self):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet

        # end exitGame

    # unregister 
    def unregister(self):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet

        # end unregister

    # guess letter
    def guessLetter(self, guessedLetter):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet

        # return new word state (if the guess was correct or not) 
        # end guessLetter

    #NOTE, not necessary, complete this later
    # guess word (optional)
    def __guessWord(self, guessedWord):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet

        # return new word state (if the guess was correct or not) 
        #end guessWord


    # select a word
    def selectWord(self, enteredWord):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet

        # handle if server rejected your word
        
        #end selectWord


    # initialize guesser 
    def initGuesser(self):
        # build the packet using our protocol 
        print("delete this later")
        # send the packet

        #end initGuesser


    # ask game state
    def askGameState():
        # build the packet using our protocol 
        print("delete this later")
        # send the packet
        
        # return game state
        #end askGameState


    ## NOTE, EC, complete this later...
    # get scoreboard
    def getScoreboard():
        # build the packet using our protocol 
        print("delete this later")
        # send the packet
        
        # return scoreboard
        #end getScoreboard


    # <end of class>

